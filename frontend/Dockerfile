# Multi-stage build: build with Node, serve with Nginx

FROM node:18-alpine AS builder
WORKDIR /app

# Install dependencies (use package-lock if present)
COPY package.json package-lock.json* ./
RUN npm ci --silent || npm install --silent

# Copy sources and build
COPY . .
RUN npm run build

# Nginx stage: serve static files
FROM nginx:stable-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
