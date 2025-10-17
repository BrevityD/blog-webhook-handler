import json
from flask import Blueprint, request, jsonify, current_app
from loguru import logger

from .git_operations import GitManager
from .post_processor import PostProcessor
from ..utils import verify_github_signature

github_webhook_bp = Blueprint('github_webhook', __name__)

@github_webhook_bp.route('/github', methods=['POST'])
def handle_github_webhook():
    """处理 GitHub Webhook 请求"""
    try:
        # 验证签名
        logger.debug(f"handler is triggered with request content: \n{request}")
        if not verify_github_signature(request):
            logger.warning("Invalid webhook signature")
            return jsonify({'error': 'Invalid signature'}), 401
        
        event_type = request.headers.get('X-GitHub-Event')
        payload = request.get_json()
        
        logger.info(f"Received GitHub event: {event_type}")
        
        # 只处理 push 事件
        if event_type == 'push':
            return handle_push_event(payload)
        else:
            logger.info(f"Ignored event type: {event_type}")
            return jsonify({'status': 'ignored', 'event': event_type}), 200
            
    except Exception as e:
        logger.error(f"Webhook processing error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

def handle_push_event(payload):
    """处理 push 事件"""
    repository = payload['repository']['full_name']
    ref = payload['ref']
    
    # 只处理主分支的推送
    if ref != 'refs/heads/main':
        logger.info(f"Ignored push to branch: {ref}")
        return jsonify({'status': 'ignored', 'reason': 'not main branch'}), 200
    
    logger.info(f"Processing push to {repository} on {ref}")
    
    # 初始化 Git 管理器
    git_manager = GitManager(
        repo_url=current_app.config['GIT_PAT_URL'].format(
            github_pat=current_app.config['GITHUB_PAT'],
            repo_name=current_app.config['GIT_REPO_NAME']
            ),
        local_path=current_app.config['GIT_LOCAL_PATH'],
        branch=current_app.config.get('GIT_BRANCH', 'main')
    )
    
    # 拉取最新代码
    try:
        git_manager.pull_latest()
        logger.info("Successfully pulled latest changes")
    except Exception as e:
        logger.error(f"Git pull failed: {str(e)}")
        return jsonify({'error': 'Git operation failed'}), 500
    
    # 处理文章
    post_processor = PostProcessor(
        source_dir=current_app.config['POSTS_SOURCE_DIR'],
        target_dir=current_app.config['POSTS_TARGET_DIR']
    )
    
    try:
        processed_count = post_processor.process_all_posts()
        logger.info(f"Successfully processed {processed_count} posts")
        
        return jsonify({
            'status': 'success',
            'processed_posts': processed_count,
            'repository': repository
        }), 200
        
    except Exception as e:
        logger.error(f"Post processing failed: {str(e)}")
        return jsonify({'error': 'Post processing failed'}), 500
