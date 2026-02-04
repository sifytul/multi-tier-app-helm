from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import mysql.connector
import redis
import json
import os

app = FastAPI(title="Backend API", version="1.0.0")

# Configuration from environment
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "app_user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "app_password")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "app_db")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

CACHE_TTL = int(os.getenv("CACHE_TTL", "300"))


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


class ItemResponse(Item):
    id: int


def get_db_connection():
    """Create database connection."""
    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )


def get_redis_client():
    """Create Redis client."""
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        decode_responses=True
    )


@app.get("/health")
def health_check():
    """Health check endpoint."""
    db_status = "healthy"
    cache_status = "healthy"

    # Check MySQL
    try:
        conn = get_db_connection()
        conn.close()
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    # Check Redis
    try:
        r = get_redis_client()
        r.ping()
    except Exception as e:
        cache_status = f"unhealthy: {str(e)}"

    return {
        "status": "healthy",
        "service": "backend-api",
        "database": db_status,
        "cache": cache_status
    }


@app.get("/items")
def list_items():
    """List all items with caching."""
    cache_key = "items:all"

    # Try cache first
    try:
        r = get_redis_client()
        cached = r.get(cache_key)
        if cached:
            return {"items": json.loads(cached), "source": "cache"}
    except Exception:
        pass

    # Fetch from database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, description, price FROM items")
    items = cursor.fetchall()
    cursor.close()
    conn.close()

    # Cache the result
    try:
        r = get_redis_client()
        r.setex(cache_key, CACHE_TTL, json.dumps(items))
    except Exception:
        pass

    return {"items": items, "source": "database"}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    """Get single item by ID with caching."""
    cache_key = f"items:{item_id}"

    # Try cache first
    try:
        r = get_redis_client()
        cached = r.get(cache_key)
        if cached:
            return {"item": json.loads(cached), "source": "cache"}
    except Exception:
        pass

    # Fetch from database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, description, price FROM items WHERE id = %s", (item_id,))
    item = cursor.fetchone()
    cursor.close()
    conn.close()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Cache the result
    try:
        r = get_redis_client()
        r.setex(cache_key, CACHE_TTL, json.dumps(item))
    except Exception:
        pass

    return {"item": item, "source": "database"}


@app.post("/items")
def create_item(item: Item):
    """Create a new item."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO items (name, description, price) VALUES (%s, %s, %s)",
        (item.name, item.description, item.price)
    )
    conn.commit()
    item_id = cursor.lastrowid
    cursor.close()
    conn.close()

    # Invalidate cache
    try:
        r = get_redis_client()
        r.delete("items:all")
    except Exception:
        pass

    return {"id": item_id, "message": "Item created successfully"}
