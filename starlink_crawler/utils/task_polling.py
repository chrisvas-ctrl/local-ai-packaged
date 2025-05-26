"""
Task polling utilities for the Starlink crawler.
This module provides functions to handle asynchronous task processing with crawl4AI.
"""

import asyncio
from typing import Any

# Import from our package
from starlink_crawler.config import CrawlerConfig

async def poll_task_result(crawler, task_id: str, config: CrawlerConfig) -> Any:
    """
    Poll for the result of an asynchronous task from crawl4AI.
    
    Args:
        crawler: AsyncWebCrawler instance
        task_id: Task ID returned by crawler.arun
        config: CrawlerConfig with polling settings
        
    Returns:
        The result of the task or None if polling times out
    """
    polls_remaining = config.max_task_polls
    
    while polls_remaining > 0:
        try:
            # Check if the task has completed
            print(f"Polling for task result (attempts remaining: {polls_remaining})...")
            result = await crawler.get_task_result(task_id)
            
            # If we got a result (not another task ID), return it
            if result and not isinstance(result, str):
                print(f"Task completed successfully after {config.max_task_polls - polls_remaining + 1} attempts")
                return result
                
            # If we got another task ID, continue polling
            polls_remaining -= 1
            if polls_remaining > 0:
                print(f"Task still processing, waiting {config.task_poll_interval}s before next check...")
                await asyncio.sleep(config.task_poll_interval)
            
        except Exception as e:
            print(f"Error polling task result: {e}")
            polls_remaining -= 1
            if polls_remaining > 0:
                await asyncio.sleep(config.task_poll_interval)
    
    print("Task polling timed out, maximum attempts reached")
    return None

async def is_task_id_response(result) -> bool:
    """
    Check if the result from crawler.arun is a task ID instead of actual content.
    
    Args:
        result: Result from crawler.arun
        
    Returns:
        bool: True if the result appears to be a task ID, False otherwise
    """
    # Task IDs are typically strings and not markdown content
    if isinstance(result, str):
        # Task IDs are usually short strings without markdown formatting
        if len(result) < 100 and not result.startswith('#') and not result.startswith('<!--'):
            return True
    return False