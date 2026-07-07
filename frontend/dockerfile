FROM node:22-alpine3.23 AS builder

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

FROM nginx:1.30.3-alpine

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
