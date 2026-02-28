# Stage 1: Build
FROM node:20-alpine AS build-stage

WORKDIR /app

# 复制依赖文件并安装
COPY package*.json ./
RUN npm install

# 复制前端代码
COPY . .

# 设置构建参数
ARG VITE_BACKEND_URL
ENV VITE_BACKEND_URL=$VITE_BACKEND_URL

# 构建前端应用 (Web 版本)
RUN npm run build:web

# Stage 2: Serve
FROM nginx:stable-alpine AS production-stage

# 从构建阶段复制构建好的静态文件
COPY --from=build-stage /app/dist-web /usr/share/nginx/html

# 复制 Nginx 配置文件
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
