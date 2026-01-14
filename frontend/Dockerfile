# Stage 1: Build image

FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json .

RUN npm ci

COPY . .

# RUN chmod +x node_modules/.bin/*

ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build

# Stage 2: Run the build

# FROM registry.redhat.io/ubi9/nginx-120
FROM nginx:alpine

ARG NODE_ENV=production
ENV NODE_ENV=$NODE_ENV

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=builder /app/dist /usr/share/nginx/html

# RUN chmod -R g+rX /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]