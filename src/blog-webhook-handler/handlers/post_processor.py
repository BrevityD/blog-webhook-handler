import os
import shutil
from pathlib import Path
from loguru import logger

class PostProcessor:
    """文章后处理器"""
    
    def __init__(self, source_dir: str, target_dir: str):
        self.source_dir = source_dir
        self.target_dir = target_dir
        # 所有支持的文件类型
        self.supported_extensions = {'.md'}
        
    def process_all_posts(self) -> int:
        """处理所有文章文件"""
        source_path = Path(self.source_dir)
        target_path = Path(self.target_dir)
        
        # 确保目标目录存在
        target_path.mkdir(parents=True, exist_ok=True)
        
        processed_count = 0
        
        # 遍历源目录中的所有文件
        for file_path in source_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.supported_extensions:
                try:
                    self._process_single_post(file_path, target_path)
                    processed_count += 1
                    logger.info(f"Processed: {file_path.name}")
                except Exception as e:
                    logger.error(f"Failed to process {file_path}: {str(e)}")
        
        logger.info(f"Total processed posts: {processed_count}")
        return processed_count
    
    def _process_single_post(self, source_file: Path, target_dir: Path):
        """处理单个文章文件"""
        # 构建目标文件路径
        post_proj_name = source_file.name.replace(source_file.suffix, "")
        target_file = target_dir / post_proj_name / ("index"+source_file.suffix)
        
        # 确保目标目录存在
        target_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 复制文件（这里可以根据需要进行内容处理）
        shutil.copy2(source_file, target_file)
        
        # 可以在这里添加更多的处理逻辑，比如：
        # - 转换 Markdown 到 HTML
        # - 添加元数据
        # - 生成摘要
        # - 图片处理等
        
        logger.debug(f"Copied {source_file} to {target_file}")
