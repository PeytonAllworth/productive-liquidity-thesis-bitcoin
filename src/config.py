"""
Configuration loader for research project.

This module loads settings from config/settings.yaml and provides
easy access to configuration values throughout the codebase.

Usage:
    from src.config import load_config
    
    cfg = load_config()
    print(cfg['events']['cyprus_2013'])  # Access event dates
    print(cfg['windows']['days_before'])  # Access window sizes
"""

import os
from pathlib import Path
from typing import Dict, Any
import yaml


def get_project_root() -> Path:
    """
    Get the absolute path to the project root directory.
    
    Returns:
        Path object pointing to project root
    """
    # This file is in src/config.py, so parent is src/, parent.parent is project root
    return Path(__file__).parent.parent


def load_config(config_path: str = None) -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Optional path to config file. If None, uses default
                    location: config/settings.yaml
    
    Returns:
        Dictionary containing all configuration settings
    
    Raises:
        FileNotFoundError: If settings.yaml doesn't exist
        yaml.YAMLError: If YAML is malformed
    
    Example:
        >>> cfg = load_config()
        >>> print(cfg['events']['cyprus_2013'])
        '2013-03-16'
    """
    if config_path is None:
        # Default: look for config/settings.yaml in project root
        project_root = get_project_root()
        config_path = project_root / "config" / "settings.yaml"
    else:
        config_path = Path(config_path)
    
    # Check if file exists
    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}\n"
            f"Did you copy config/settings.example.yaml to config/settings.yaml?"
        )
    
    # Load YAML
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Validate required keys (basic check)
    required_keys = ['data', 'events', 'windows']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required config section: {key}")
    
    return config


def get_data_paths(config: Dict[str, Any]) -> Dict[str, Path]:
    """
    Convert relative data paths in config to absolute Path objects.
    
    Args:
        config: Configuration dictionary from load_config()
    
    Returns:
        Dictionary with keys: 'raw', 'processed', 'figures'
        Values are absolute Path objects
    
    Example:
        >>> cfg = load_config()
        >>> paths = get_data_paths(cfg)
        >>> print(paths['raw'])
        PosixPath('/Users/peytonallworth/projects/.../data/raw')
    """
    project_root = get_project_root()
    
    return {
        'raw': project_root / config['data']['out_raw'],
        'processed': project_root / config['data']['out_processed'],
        'figures': project_root / config['data']['out_figures']
    }


def get_event_date(config: Dict[str, Any], event_name: str) -> str:
    """
    Get the anchor date for a specific event.
    
    Args:
        config: Configuration dictionary
        event_name: Name of event (e.g., 'cyprus_2013')
    
    Returns:
        Date string in YYYY-MM-DD format
    
    Raises:
        KeyError: If event_name not found in config
    """
    if event_name not in config['events']:
        available = ', '.join(config['events'].keys())
        raise KeyError(
            f"Event '{event_name}' not found in config. "
            f"Available events: {available}"
        )
    
    return config['events'][event_name]


# Convenience: Load config on import (users can call load_config() explicitly if needed)
try:
    CONFIG = load_config()
except FileNotFoundError:
    # If settings.yaml doesn't exist yet, set CONFIG to None
    # This allows imports without errors during initial setup
    CONFIG = None

