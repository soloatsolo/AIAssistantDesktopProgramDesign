import json
import os
from typing import Dict, Any, Optional

class Config:
    DEFAULT_CONFIG = {
        "character": {
            "gender": "female",
            "style": "anime",
        },
        "ai": {
            "model": "gpt-4-turbo-preview",
            "temperature": 0.7,
        },
        "voice": {
            "enabled": True,
            "volume": 1.0,
            "rate": 150,
        },
        "window": {
            "position_x": 100,
            "position_y": 100,
            "width": 300,
            "height": 400,
        }
    }
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults to ensure all fields exist
                    return self._merge_configs(self.DEFAULT_CONFIG, loaded_config)
        except Exception as e:
            print(f"Error loading config: {e}")
        
        # Return default config if loading fails
        return self.DEFAULT_CONFIG.copy()
    
    def save_config(self) -> bool:
        """Save current configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key (dot notation supported)"""
        try:
            value = self.config
            for k in key.split('.'):
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> bool:
        """Set a configuration value by key (dot notation supported)"""
        try:
            keys = key.split('.')
            target = self.config
            for k in keys[:-1]:
                target = target[k]
            target[keys[-1]] = value
            return True
        except (KeyError, TypeError):
            return False
    
    @staticmethod
    def _merge_configs(default: Dict, custom: Dict) -> Dict:
        """Recursively merge custom config with default config"""
        result = default.copy()
        for key, value in custom.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = Config._merge_configs(result[key], value)
            else:
                result[key] = value
        return result