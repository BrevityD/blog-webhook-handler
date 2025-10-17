import subprocess
from pathlib import Path
from typing import Optional
from loguru import logger

class GitManager:
    """Git 操作管理器"""
    
    def __init__(self, repo_url: str, local_path: str, branch: str = 'main'):
        self.repo_url = repo_url
        self.local_path = Path(local_path)
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
    
    def _clone_or_pull(self):
        """克隆仓库"""
        if not self.local_path.exists():
            self.local_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Cloning repository to {self.local_path.as_posix()}")
            self._run_git_command([
                'git', 'clone', 
                '--branch', self.branch,
                self.repo_url, 
                self.local_path.as_posix()
            ])
        else:
            logger.info(f"Pulling repository to {self.local_path.as_posix()}")
            self._run_git_command(
                command = [
                    'git', 'pull',
                    self.repo_url
                ],
                cwd = self.local_path.as_posix()
            )
    
    def pull_latest(self):
        """拉取最新代码"""
        # 确保仓库存在
        self._clone_or_pull()
        logger.info("Successfully pulled latest changes")

