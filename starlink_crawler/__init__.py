"""
Starlink Crawler Package

A modular web crawler designed to process URLs from a Starlink sitemap in parallel,
extract content from web pages, and convert them to markdown files.
"""

__version__ = '0.1.0'

# Import key classes for easier access
from starlink_crawler.config import TitleStrategy, CrawlerConfig
from starlink_crawler.utils import (
    ErrorInfo, CrawlStats,
    poll_task_result, is_task_id_response,
    get_processed_urls
)
from starlink_crawler.core import RateLimiter, crawl_parallel_with_rate_limiting
from starlink_crawler.parsers import (
    extract_title_from_markdown, generate_safe_filename,
    parse_xml_file, get_urls_from_source
)

__all__ = [
    'TitleStrategy', 'CrawlerConfig',
    'ErrorInfo', 'CrawlStats',
    'RateLimiter', 'crawl_parallel_with_rate_limiting',
    'poll_task_result', 'is_task_id_response',
    'get_processed_urls',
    'extract_title_from_markdown', 'generate_safe_filename',
    'parse_xml_file', 'get_urls_from_source'
]
