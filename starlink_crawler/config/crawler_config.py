"""
Configuration class for the Starlink crawler.
This module defines the configuration settings for the crawler.
"""

import os
from typing import Optional
from crawl4ai import CacheMode

# Import from our package
from starlink_crawler.config.title_strategy import TitleStrategy

class CrawlerConfig:
    """Configuration class for crawler settings"""
    def __init__(
        self,
        max_concurrent: int = 5,              # Max concurrent browser sessions 
        memory_threshold: float = 70.0,       # Memory threshold percentage
        min_batch_delay: float = 2.0,         # Minimum delay between batches in seconds
        max_batch_delay: float = 5.0,         # Maximum delay between batches in seconds
        dynamic_delay: bool = True,           # Whether to use dynamic delays between batches
        request_rate: float = 0.2,            # Requests per second (1/5 = 0.2 for 5 second delay)
        burst: int = 2,                       # Burst capacity for rate limiter
        max_crawls_per_minute: int = 100,     # Max crawls per minute (0 = no limit)
        output_dir: Optional[str] = None,     # Output directory for markdown files
        cache_mode: CacheMode = CacheMode.BYPASS,  # Cache mode
        title_strategy: str = TitleStrategy.HEADING_FIRST,  # Title extraction strategy
        skip_existing: bool = True,           # Whether to skip already processed URLs
        task_poll_interval: float = 5.0,      # Interval between task polling attempts in seconds
        max_task_polls: int = 5               # Maximum number of task polling attempts
    ):
        """Initialize crawler configuration with default values.
        
        Args:
            max_concurrent: Maximum number of concurrent browser sessions
            memory_threshold: Memory threshold percentage to pause crawling
            min_batch_delay: Minimum delay between batches in seconds
            max_batch_delay: Maximum delay between batches in seconds
            dynamic_delay: Whether to use dynamic delays between batches
            request_rate: Requests per second (1/5 = 0.2 for 5 second delay)
            burst: Burst capacity for rate limiter
            max_crawls_per_minute: Max crawls per minute (0 = no limit)
            output_dir: Output directory for markdown files
            cache_mode: Cache mode for the crawler
            title_strategy: Title extraction strategy
            skip_existing: Whether to skip already processed URLs
            task_poll_interval: Interval between task polling attempts in seconds
            max_task_polls: Maximum number of task polling attempts
        """
        self.max_concurrent = max_concurrent
        self.memory_threshold = memory_threshold
        self.min_batch_delay = min_batch_delay
        self.max_batch_delay = max_batch_delay
        self.dynamic_delay = dynamic_delay
        self.request_rate = request_rate
        self.burst = burst
        self.max_crawls_per_minute = max_crawls_per_minute
        self.output_dir = output_dir
        self.cache_mode = cache_mode
        self.title_strategy = title_strategy
        self.skip_existing = skip_existing
        self.task_poll_interval = task_poll_interval
        self.max_task_polls = max_task_polls

        # Create output directory if specified
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)