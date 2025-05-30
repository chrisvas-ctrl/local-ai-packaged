"""
Configuration persistence utilities for the Starlink crawler and markdown cleaner.
This module provides functions to save and load configuration settings.
"""

import os
import json
from typing import Dict, Any, Optional

# Import from our package
from starlink_crawler.config import CrawlerConfig
from starlink_crawler.config.cleaner_config import CleanerConfig

# Default locations for saved configs
DEFAULT_CONFIG_PATH = os.path.expanduser("~/.starlink_crawler_config.json")
DEFAULT_CLEANER_CONFIG_PATH = os.path.expanduser("~/.starlink_cleaner_config.json")

def save_config(config: CrawlerConfig, filepath: str = DEFAULT_CONFIG_PATH) -> bool:
    """
    Save crawler configuration to a JSON file.
    
    Args:
        config: CrawlerConfig instance to save
        filepath: Path to save the configuration file (default: ~/.starlink_crawler_config.json)
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Convert config object to dictionary
        config_dict = {
            "max_concurrent": config.max_concurrent,
            "memory_threshold": config.memory_threshold,
            "min_batch_delay": config.min_batch_delay,
            "max_batch_delay": config.max_batch_delay,
            "delay_type": config.delay_type,
            "min_request_delay": config.min_request_delay,
            "max_request_delay": config.max_request_delay,
            "request_rate": config.request_rate,
            "burst": config.burst,
            "max_crawls_per_minute": config.max_crawls_per_minute,
            "title_strategy": config.title_strategy,
            "skip_existing": config.skip_existing,
            "task_poll_interval": config.task_poll_interval,
            "max_task_polls": config.max_task_polls
        }
        
        # Save to file
        with open(filepath, 'w') as f:
            json.dump(config_dict, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error saving configuration: {e}")
        return False

def load_config(filepath: str = DEFAULT_CONFIG_PATH) -> Optional[Dict[str, Any]]:
    """
    Load crawler configuration from a JSON file.
    
    Args:
        filepath: Path to the configuration file (default: ~/.starlink_crawler_config.json)
        
    Returns:
        dict: Configuration dictionary or None if file doesn't exist or is invalid
    """
    if not os.path.exists(filepath):
        return None
    
    try:
        with open(filepath, 'r') as f:
            config_dict = json.load(f)
        return config_dict
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return None

def create_config_from_dict(config_dict: Dict[str, Any], output_dir: str = None) -> CrawlerConfig:
    """
    Create a CrawlerConfig instance from a configuration dictionary.
    
    Args:
        config_dict: Dictionary containing configuration values
        output_dir: Output directory for markdown files (optional)
        
    Returns:
        CrawlerConfig: Configuration instance
    """
    # Create a copy of the dict to avoid modifying the original
    config = dict(config_dict)
    
    # Add output_dir if provided
    if output_dir:
        config["output_dir"] = output_dir
    
    # Create and return config instance
    return CrawlerConfig(**config)


def save_cleaner_config(config: CleanerConfig, filepath: str = DEFAULT_CLEANER_CONFIG_PATH) -> bool:
    """
    Save cleaner configuration to a JSON file.
    
    Args:
        config: CleanerConfig instance to save
        filepath: Path to save the configuration file (default: ~/.starlink_cleaner_config.json)
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Convert config object to dictionary
        config_dict = {
            "input_dir": config.input_dir,
            "output_dir": config.output_dir,
            "extract_metadata": config.extract_metadata,
            "fix_urls": config.fix_urls,
            "remove_navigation": config.remove_navigation,
            "remove_footer": config.remove_footer,
            "add_frontmatter": config.add_frontmatter,
            "language": config.language,
            "batch_mode": config.batch_mode,
            "pattern": config.pattern,
            "limit": config.limit
        }
        
        # Save to file
        with open(filepath, 'w') as f:
            json.dump(config_dict, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error saving cleaner configuration: {e}")
        return False


def load_cleaner_config(filepath: str = DEFAULT_CLEANER_CONFIG_PATH) -> Optional[Dict[str, Any]]:
    """
    Load cleaner configuration from a JSON file.
    
    Args:
        filepath: Path to the configuration file (default: ~/.starlink_cleaner_config.json)
        
    Returns:
        dict: Configuration dictionary or None if file doesn't exist or is invalid
    """
    if not os.path.exists(filepath):
        return None
    
    try:
        with open(filepath, 'r') as f:
            config_dict = json.load(f)
        return config_dict
    except Exception as e:
        print(f"Error loading cleaner configuration: {e}")
        return None


def create_cleaner_config_from_dict(config_dict: Dict[str, Any], input_dir: str = None, output_dir: str = None) -> CleanerConfig:
    """
    Create a CleanerConfig instance from a configuration dictionary.
    
    Args:
        config_dict: Dictionary containing configuration values
        input_dir: Input directory for markdown files (optional)
        output_dir: Output directory for processed files (optional)
        
    Returns:
        CleanerConfig: Configuration instance
    """
    # Create a copy of the dict to avoid modifying the original
    config = dict(config_dict)
    
    # Add input_dir and output_dir if provided
    if input_dir:
        config["input_dir"] = input_dir
    if output_dir:
        config["output_dir"] = output_dir
    
    # Create and return config instance
    return CleanerConfig(**config)
