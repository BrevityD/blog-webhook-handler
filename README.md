# Blog Webhook Handler

A Flask-based GitHub Webhook handler for automatic blog post deployment.

## Features

- ✅ Receive GitHub Webhook push events
- ✅ Automatically pull latest blog repository code
- ✅ Process Markdown format blog posts
- ✅ Secure GitHub Webhook signature verification
- ✅ Support Docker containerized deployment
- ✅ Flexible configuration file management

## Quick Start

### 1. Configure GitHub Webhook

1. In your GitHub blog repository, go to Settings → Webhooks → Add webhook
2. Configure Payload URL: `http://your-server-ip:5000/webhook/github`
3. Select Content type: `application/json`
4. Set Secret: Match with `github.webhook_secret` in config file
5. Select trigger events: Only select `push` events

### 2. Configure Application

Edit `config/default.json` file:

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

### 3. Deployment Methods

#### Using Docker Compose (Recommended)

```bash
# Build and start service
docker-compose up -d

# View logs
docker-compose logs -f
```

#### Direct Run

```bash
# Install dependencies
pip install -e .

# Start service
python -m src.blog-webhook-handler.app
```

## Project Structure

```
blog-webhook-handler/
├── src/blog-webhook-handler/
│   ├── app.py                 # Main application entry
│   ├── handlers/
│   │   ├── github_webhook.py  # GitHub Webhook handler
│   │   ├── git_operations.py  # Git operations manager
│   │   └── post_processor.py  # Post processor
│   ├── models/
│   │   └── webhook_models.py  # Data models
│   └── utils/
│       ├── config_loader.py   # Configuration loader
│       └── security.py        # Security verification
├── config/
│   └── default.json           # Default configuration file
├── logs/                      # Log directory
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

## Workflow

1. **Push Event Trigger**: When new commits are pushed to GitHub blog repository
2. **Webhook Reception**: Server receives GitHub Webhook request
3. **Security Verification**: Verify Webhook signature for request legitimacy
4. **Code Pull**: Automatically pull latest blog repository code
5. **Post Processing**: Process Markdown files and copy to target directory
6. **Response Return**: Return processing result to GitHub

## Configuration Guide

### Server Configuration
- `server.host`: Service listening address (default: 0.0.0.0)
- `server.port`: Service listening port (default: 5000)
- `server.debug`: Debug mode (set to false for production)

### GitHub Configuration
- `github.webhook_secret`: GitHub Webhook secret
- `github.repo_url`: Blog repository Git URL
- `github.local_path`: Local cloned repository path
- `github.branch`: Branch to track (default: main)

### Posts Configuration
- `posts.source_dir`: Source posts directory (path in repository)
- `posts.target_dir`: Target posts directory (deployment path)

## Development

### Local Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows

# Install dependencies
pip install -e .

# Start development server
python -m src.blog-webhook-handler.app
```

### Testing Webhook

You can use curl to simulate GitHub Webhook:

```bash
curl -X POST http://localhost:5000/webhook/github \
  -H "Content-Type: application/json" \
  -H "X-GitHub-Event: push" \
  -H "X-Hub-Signature-256: sha256=..." \
  -d '{"ref":"refs/heads/main","repository":{"full_name":"your-username/your-repo"}}'
```

## License

MIT License
