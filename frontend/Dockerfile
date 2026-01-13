# Stage 1: Build image

FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json .

RUN npm ci

COPY . .

RUN chmod +x node_modules/.bin/*

RUN npm run build

# Stage 2: Run the build

FROM registry.redhat.io/ubi9/nginx-120

COPY nginx.conf /etc/nginx/conf.d/nginx.conf

COPY --from=builder /app/dist /usr/share/nginx/html

RUN chmod -R g+rX /usr/share/nginx/html

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]