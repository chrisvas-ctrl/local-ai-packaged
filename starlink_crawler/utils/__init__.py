"""
Utility modules for the Starlink crawler.
"""

from starlink_crawler.utils.error_handling import ErrorInfo
from starlink_crawler.utils.stats import CrawlStats
from starlink_crawler.utils.task_polling import poll_task_result, is_task_id_response
from starlink_crawler.utils.url_processing import get_processed_urls

__all__ = [
    'ErrorInfo', 'CrawlStats',
    'poll_task_result', 'is_task_id_response',
    'get_processed_urls'
]
