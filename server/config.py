from pathlib import Path
import toml

class Config:    
    _toml_config = None
    
    @staticmethod
    def load_toml_config():
        file_path = "config.toml"
        with open(file_path, "r") as f:
            Config._toml_config = toml.load(f)
            
    @staticmethod
    def get(section, key, default=None):
        if Config._toml_config:
            value = Config._toml_config.get(section, {}).get(key, default)
            if value is not None:
                return value
        return default
    
Config.load_toml_config()