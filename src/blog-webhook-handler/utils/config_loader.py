import json
import os
from pathlib import Path
from typing import Dict, Any

class ConfigLoader:
    """配置加载器"""
    
    def __init__(self, config_dir: str = "config", file_name: str = "default.json"):
        self.config_dir = Path(config_dir)
        self._config = {}
        self.load_config(file_name=file_name)
    
    def load_config(self, file_name: str = "default.json"):
        """加载配置文件"""
        default_config_path = self.config_dir / file_name
        
        if not default_config_path.exists():
            raise FileNotFoundError(f"Default config file not found: {default_config_path}")
        
        with open(default_config_path, 'r', encoding='utf-8') as f:
            self._config = json.load(f)
        
        # 可以在这里添加环境特定的配置覆盖逻辑
        # 例如：development.json, production.json 等
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_all(self) -> Dict[str, Any]:
        """获取所有配置"""
        return self._config.copy()
