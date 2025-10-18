import os
import json
import re
import shutil
import time
import yaml
from pathlib import Path
from loguru import logger

class PostProcessor:
    """文章后处理器"""
    
    def __init__(self, source_dir: str, target_dir: str):
        self.source_dir = source_dir
        self.target_dir = target_dir
        # 所有支持的文件类型
        self.supported_extensions = {'.md'}
        self.supported_assets = {'.jpg', '.jpeg', '.png'}
        
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
        proj_name = source_file.parent.name
        proj_name = re.sub(r'[^\w\u4e00-\u9fff]', '', proj_name)
        target_file = target_dir / proj_name / ("index"+source_file.suffix)
        target_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, target_file)
        logger.debug(f"Copied {source_file} to {target_file}")
        for file_path in source_file.parent.glob("*"):
            if file_path.is_file() and file_path.suffix.lower() in self.supported_assets:
                source_asset = file_path
                target_asset = target_dir / proj_name / source_asset.name
                shutil.copy2(source_asset, target_asset)
                logger.debug(f"Copied {source_asset} to {target_asset}")

        self._process_post_content(source_file, target_file)
        logger.info(f"An article is created: {target_file}")
    
    def _process_post_content(self, source_file: Path, target_file: Path):
        """处理单个post的文件头等"""
        post_config_file = source_file.parent / "config.json"
        post_config = {
            "title": source_file.parent.name,
            "description": "结垒发布了一篇文章\n该描述由BrevityD/blog-webhook-handler自动生成，点个star求求了",
            "date": time.strftime("%Y-%m-%d", time.localtime(time.time()+60*60*8)),
            "lastmod": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()+60*60*8))
        }
        if post_config_file.exists():
            with open(post_config_file, "r", encoding="utf8") as f:
                post_config.update(json.load(f))
        header = self._post_config2header(post_config)
        with open(target_file, "r+") as wf:
            old = wf.read()
            wf.seek(0)
            wf.write(header)
            wf.write(old)
        logger.debug(f"Article {target_file.parent.name} with header {header}")
        
    
    def _post_config2header(self, post_config):
        header = "---\n{config}---\n\n"
        config = yaml.dump(post_config, allow_unicode=True, sort_keys=False)
        header = header.format(config=config)
        return header
