FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端代码
COPY . .

# 暴露端口（默认8000，可以通过环境变量修改）
EXPOSE 8000

# 启动命令
# 使用 uvicorn 启动，支持通过环境变量控制 host 和 port
CMD ["python", "main.py"]
