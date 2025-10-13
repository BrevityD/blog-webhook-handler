FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖
RUN sed -i 's@//.*archive.ubuntu.com@//mirrors.ustc.edu.cn@g' /etc/apt/sources.list \
    && apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY ./ ./

# 安装 Python 依赖
RUN pip install --no-cache-dir -e .

# 创建日志目录
RUN mkdir -p logs

# 暴露端口
EXPOSE 5000

# 启动应用
CMD ["python", "-m", "src.blog-webhook-handler.app"]
