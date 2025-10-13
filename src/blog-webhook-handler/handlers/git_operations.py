import os
import subprocess
from typing import Optional
from loguru import logger

class GitManager:
    """Git 操作管理器"""
    
    def __init__(self, repo_url: str, local_path: str, branch: str = 'main'):
        self.repo_url = repo_url
        self.local_path = local_path
        self.branch = branch
        
    def _run_git_command(self, command: list, cwd: Optional[str] = None) -> str:
        """运行 Git 命令"""
        try:
            result = subprocess.run(
                command,
                cwd=cwd or self.local_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"Git command failed: {e.stderr}")
            raise
    
    def clone_if_not_exists(self):
        """如果本地目录不存在，则克隆仓库"""
        if not os.path.exists(self.local_path):
            logger.info(f"Cloning repository to {self.local_path}")
            os.makedirs(os.path.dirname(self.local_path), exist_ok=True)
            self._run_git_command([
                'git', 'clone', 
                '--branch', self.branch,
                self.repo_url, 
                self.local_path
            ])
        else:
            logger.info(f"Repository already exists at {self.local_path}")
    
    def pull_latest(self):
        """拉取最新代码"""
        # 确保仓库存在
        self.clone_if_not_exists()
        
        logger.info(f"Pulling latest changes from {self.branch}")
        
        # 获取当前分支
        current_branch = self._run_git_command(['git', 'branch', '--show-current'])
        
        # 如果不在目标分支，切换到目标分支
        if current_branch != self.branch:
            logger.info(f"Switching from {current_branch} to {self.branch}")
            self._run_git_command(['git', 'checkout', self.branch])
        
        # 拉取最新代码
        self._run_git_command(['git', 'pull', 'origin', self.branch])
        
        logger.info("Successfully pulled latest changes")
    
    def get_latest_commit_hash(self) -> str:
        """获取最新提交的哈希值"""
        return self._run_git_command(['git', 'rev-parse', 'HEAD'])
