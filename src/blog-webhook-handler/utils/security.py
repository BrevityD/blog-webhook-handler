import hmac
import hashlib
from flask import Request, current_app

def verify_github_signature(request: Request) -> bool:
    """验证 GitHub Webhook 签名"""
    signature = request.headers.get('X-Hub-Signature-256')
    if not signature:
        return False
    
    # 从应用配置中获取密钥
    secret = current_app.config.get('GITHUB_WEBHOOK_SECRET')
    if not secret:
        # 如果没有配置密钥，跳过验证（仅用于开发环境）
        return True
    
    # 计算 HMAC SHA256
    body = request.get_data()
    computed_signature = 'sha256=' + hmac.new(
        secret.encode('utf-8'),
        body,
        hashlib.sha256
    ).hexdigest()
    
    # 使用 hmac.compare_digest 来防止时序攻击
    return hmac.compare_digest(signature, computed_signature)
