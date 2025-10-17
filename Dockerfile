FROM docker.1ms.run/library/python:3.12-slim

WORKDIR /app

# 安装系统依赖
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources \
    && apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制项目文件
COPY ./ ./
# 复制github ssh key

# 安装 Python 依赖
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ \
    && pip install -e .

# 创建日志目录
RUN mkdir -p logs

# 暴露端口
EXPOSE 13134

# 启动应用
CMD ["python", "-m", "src.blog-webhook-handler.app"]
