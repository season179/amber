"""
Configuration utilities for Amber.txt
"""
import os
import yaml
from typing import Dict, Any, Optional
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


def get_env_var(name: str, default: Optional[str] = None) -> str:
    """
    Get an environment variable or return a default value.
    
    Args:
        name: Name of environment variable
        default: Default value if not found
        
    Returns:
        Value of environment variable or default
    """
    value = os.environ.get(name, default)
    if value is None:
        raise ValueError(f"Environment variable {name} not set and no default provided")
    return value


def get_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Args:
        config_path: Path to config file
        
    Returns:
        Configuration dictionary
    """
    if not os.path.exists(config_path):
        return {}
        
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)
    
    
def get_openrouter_api_key() -> str:
    """
    Get the OpenRouter API key from environment variables.
    
    Returns:
        OpenRouter API key
    """
    return get_env_var("OPENROUTER_API_KEY")


def get_default_model() -> str:
    """
    Get the default LLM model to use.
    
    Returns:
        Model identifier
    """
    return get_env_var("DEFAULT_MODEL", "openai/gpt-3.5-turbo")


def get_storage_dir() -> str:
    """
    Get the storage directory for memories.
    
    Returns:
        Path to storage directory
    """
    return get_env_var("STORAGE_DIR", "memory_store")


def get_storage_format() -> str:
    """
    Get the storage format for memories.
    
    Returns:
        Storage format ("json" or "yaml")
    """
    return get_env_var("STORAGE_FORMAT", "json")