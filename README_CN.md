# 博客 Webhook 处理器

一个基于 Flask 的 GitHub Webhook 处理器，用于自动部署博客文章。

## 功能特性

- ✅ 接收 GitHub Webhook 推送事件
- ✅ 自动拉取博客仓库最新代码
- ✅ 处理 Markdown 格式的博客文章
- ✅ 安全验证 GitHub Webhook 签名
- ✅ 支持 Docker 容器化部署
- ✅ 灵活的配置文件管理

## 快速开始

### 1. 配置 GitHub Webhook

1. 在您的 GitHub 博客仓库中，进入 Settings → Webhooks → Add webhook
2. 配置 Payload URL: `http://your-server-ip:5000/webhook/github`
3. 选择 Content type: `application/json`
4. 设置 Secret: 与配置文件中的 `github.webhook_secret` 保持一致
5. 选择触发事件: 仅选择 `push` 事件

### 2. 配置应用

编辑 `config/default.json` 文件：

```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": false,
    "secret_key": "your-secret-key-here"
  },
  "github": {
    "webhook_secret": "your-github-webhook-secret-here",
    "repo_url": "https://github.com/your-username/your-blog-repo.git",
    "local_path": "/tmp/blog-repo",
    "branch": "main"
  },
  "posts": {
    "source_dir": "/tmp/blog-repo/posts",
    "target_dir": "/var/www/blog/posts"
  },
  "logging": {
    "level": "INFO",
    "file": "logs/webhook.log",
    "rotation": "10 MB"
  }
}
```

### 3. 部署方式

#### 使用 Docker Compose（推荐）

```bash
# 构建并启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

#### 直接运行

```bash
# 安装依赖
pip install -e .

# 启动服务
python -m src.blog-webhook-handler.app
```

## 项目结构

```
blog-webhook-handler/
├── src/blog-webhook-handler/
│   ├── app.py                 # 主应用入口
│   ├── handlers/
│   │   ├── github_webhook.py  # GitHub Webhook 处理器
│   │   ├── git_operations.py  # Git 操作管理
│   │   └── post_processor.py  # 文章后处理器
│   ├── models/
│   │   └── webhook_models.py  # 数据模型
│   └── utils/
│       ├── config_loader.py   # 配置加载器
│       └── security.py        # 安全验证
├── config/
│   └── default.json           # 默认配置文件
├── logs/                      # 日志目录
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

## 工作流程

1. **推送事件触发**: 当有新的提交推送到 GitHub 博客仓库时
2. **Webhook 接收**: 服务器接收 GitHub 发送的 Webhook 请求
3. **安全验证**: 验证 Webhook 签名确保请求合法性
4. **代码拉取**: 自动拉取博客仓库的最新代码
5. **文章处理**: 处理 Markdown 文件并复制到目标目录
6. **响应返回**: 返回处理结果给 GitHub

## 配置说明

### 服务器配置
- `server.host`: 服务监听地址（默认: 0.0.0.0）
- `server.port`: 服务监听端口（默认: 5000）
- `server.debug`: 调试模式（生产环境设为 false）

### GitHub 配置
- `github.webhook_secret`: GitHub Webhook 密钥
- `github.repo_url`: 博客仓库的 Git URL
- `github.local_path`: 本地克隆仓库的路径
- `github.branch`: 要跟踪的分支（默认: main）

### 文章配置
- `posts.source_dir`: 源文章目录（在仓库中的路径）
- `posts.target_dir`: 目标文章目录（部署后的路径）

## 开发

### 本地开发环境

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -e .

# 启动开发服务器
python -m src.blog-webhook-handler.app
```

### 测试 Webhook

可以使用 curl 模拟 GitHub Webhook：

```bash
curl -X POST http://localhost:5000/webhook/github \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: push" \
  -H "X-Hub-Signature-256: sha256=..." \
  -d '{"ref":"refs/heads/main","repository":{"full_name":"your-username/your-repo"}}'
```

## 许可证

MIT License
