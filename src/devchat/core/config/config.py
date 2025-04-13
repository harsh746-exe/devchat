import os
from pathlib import Path
from typing import Dict, Optional
import yaml
from pydantic import BaseModel

class Config(BaseModel):
    """Configuration model for DevChat"""
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2000
    api_key: Optional[str] = None
    huggingface_token: Optional[str] = None

class ConfigManager:
    """Manages DevChat configuration"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".devchat"
        self.config_file = self.config_dir / "config.yaml"
        self.config = Config()
        
    def setup(self) -> None:
        """Set up initial configuration"""
        self.config_dir.mkdir(exist_ok=True)
        if not self.config_file.exists():
            self.save_config()
            
    def load_config(self) -> None:
        """Load configuration from file"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                config_data = yaml.safe_load(f) or {}
                self.config = Config(**config_data)
                
    def save_config(self) -> None:
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            yaml.dump(self.config.dict(), f)
            
    def get(self, key: str) -> Optional[str]:
        """Get a configuration value"""
        return getattr(self.config, key, None)
    
    def set(self, key: str, value: str) -> None:
        """Set a configuration value"""
        if hasattr(self.config, key):
            setattr(self.config, key, value)
            self.save_config()
            
    def list_all(self) -> Dict[str, str]:
        """List all configuration values"""
        return self.config.dict() 