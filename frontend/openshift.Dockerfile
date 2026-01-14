# Stage 1: Build
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .

RUN chmod +x node_modules/.bin/*

RUN npm run build

# Stage 2: Runtime
FROM nginx:alpine

# Main nginx config
COPY openshift.nginx.conf /etc/nginx/nginx.conf

# Server block
COPY openshift.default.conf /etc/nginx/conf.d/default.conf

# Just copy files – do NOT chmod/chgrp
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
