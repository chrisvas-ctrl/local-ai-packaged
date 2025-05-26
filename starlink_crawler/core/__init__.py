"""
Core functionality for the Starlink crawler.
"""

from starlink_crawler.core.rate_limiting import RateLimiter
from starlink_crawler.core.crawler import crawl_parallel_with_rate_limiting

__all__ = ['RateLimiter', 'crawl_parallel_with_rate_limiting']
