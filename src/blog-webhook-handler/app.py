from flask import Flask
from loguru import logger
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from .handlers import github_webhook_bp
from .utils import ConfigLoader

def setup_logging():
    """配置日志"""
    config = ConfigLoader()

    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=config.get('logging.level', 'INFO')
    )
    logger.add(
        config.get('logging.file', 'logs/webhook.log'),
        rotation=config.get('logging.rotation', '10 MB'),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=config.get('logging.level', 'INFO')
    )

def create_app():
    """创建 Flask 应用"""
    config = ConfigLoader()
    app = Flask(__name__)
    
    # 从配置文件加载设置
    app.config['SECRET_KEY'] = config.get('server.secret_key', 'dev-secret-key')
    
    # GitHub Webhook 配置
    app.config['GIT_PAT_URL'] = config.get('github.pat_url')
    app.config['GIT_REPO_NAME'] = config.get('github.repo_name')
    app.config['GIT_LOCAL_PATH'] = config.get('github.local_path')
    app.config['GIT_BRANCH'] = config.get('github.branch', 'main')
    
    # 文章处理配置
    app.config['POSTS_SOURCE_DIR'] = config.get('posts.source_dir')
    app.config['POSTS_TARGET_DIR'] = config.get('posts.target_dir')
    
    # GitHub Webhook 密钥（用于安全验证）
    app.config['GITHUB_WEBHOOK_SECRET'] = config.get('github.webhook_secret')
    app.config['GITHUB_PAT'] = config.get('github.personal_access_token')
    
    # 注册蓝图
    app.register_blueprint(github_webhook_bp, url_prefix='/webhook')
    
    @app.route('/')
    def hello_world():
        logger.info(f"hello world is triggered")
        return 'Blog Webhook Handler is running!'
    
    @app.route('/health')
    def health_check():
        logger.info(f"health is triggered")
        return {'status': 'healthy'}, 200
    
    return app

if __name__ == '__main__':
    import json
    setup_logging()
    app = create_app()
    config = ConfigLoader()
    logger.info("Starting Blog Webhook Handler...")
    
    host = config.get('server.host', '0.0.0.0')
    port = config.get('server.port', 13134)
    debug = config.get('server.debug', False)
    
    logger.info(f"Server will start on {host}:{port}")
    logger.info(f"Server is started with configs:{json.dumps(config._config, indent=4)}")
    app.run(host=host, port=port, debug=debug)
