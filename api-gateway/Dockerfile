FROM node:20-alpine

WORKDIR /app

ENV NODE_ENV=production

COPY package.json ./
RUN npm install --production

COPY src/ ./src/

EXPOSE 5000

USER node

CMD ["npm", "start"]
