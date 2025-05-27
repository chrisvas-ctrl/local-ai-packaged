"""
Test script for the Starlink crawler package.
This script tests the basic functionality of the package.
"""

import os
import asyncio
import sys

# Add the parent directory to the path so we can import the package
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from starlink_crawler.config import CrawlerConfig, TitleStrategy
from starlink_crawler.core import crawl_parallel_with_rate_limiting
from starlink_crawler.parsers import get_urls_from_source
from starlink_crawler.utils.stats import CrawlStats
from starlink_crawler.utils.error_handling import ErrorInfo

# Set up output directory
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_output")
os.makedirs(output_dir, exist_ok=True)

async def test_sitemap_parser():
    """Test the sitemap parser functionality."""
    print("\n=== Testing Sitemap Parser ===")
    
    # Test with a small sitemap URL
    test_url = "https://support.skydio.com/hc/sitemap.xml"
    print(f"Fetching URLs from: {test_url}")
    
    try:
        urls = await get_urls_from_source('url', test_url)
        print(f"Successfully retrieved {len(urls)} URLs")
        
        # Print the first 5 URLs
        if urls:
            print("First 5 URLs:")
            for i, url in enumerate(urls[:5]):
                print(f"  {i+1}. {url}")
        
        return urls
    except Exception as e:
        print(f"Error testing sitemap parser: {str(e)}")
        return []

async def test_crawler(urls):
    """Test the crawler functionality with a small batch of URLs."""
    if not urls:
        print("No URLs to test crawler with. Skipping crawler test.")
        return
    
    print("\n=== Testing Crawler ===")
    
    # Create a test configuration with conservative settings
    config = CrawlerConfig(
        max_concurrent=2,
        memory_threshold=70.0,
        min_batch_delay=1.0,
        max_batch_delay=2.0,
        dynamic_delay=True,
        request_rate=0.5,  # 1 request every 2 seconds
        burst=1,
        max_crawls_per_minute=10,
        output_dir=output_dir,
        title_strategy=TitleStrategy.HEADING_FIRST,
        skip_existing=False,
        task_poll_interval=2.0,
        max_task_polls=10
    )
    
    # Test with just 3 URLs to keep the test quick
    test_batch = urls[:3]
    print(f"Testing crawler with {len(test_batch)} URLs")
    
    try:
        success, failed = await crawl_parallel_with_rate_limiting(test_batch, config)
        print(f"Crawler test complete! Success: {success}, Failed: {failed}")
        
        # Check if files were created
        files = os.listdir(output_dir)
        md_files = [f for f in files if f.endswith('.md')]
        print(f"Created {len(md_files)} markdown files in {output_dir}")
        
        return success, failed
    except Exception as e:
        print(f"Error testing crawler: {str(e)}")
        return 0, 0

async def test_error_handling():
    """Test the error handling functionality."""
    print("\n=== Testing Error Handling ===")
    
    # Test error code extraction and explanation
    test_errors = [
        "status=404 Not Found",
        "status=429 Too Many Requests",
        "status=500 Internal Server Error",
        "net::ERR_CONNECTION_REFUSED",
        "Unknown error occurred"
    ]
    
    for error_msg in test_errors:
        error_code, explanation = ErrorInfo.get_error_explanation(error_msg)
        print(f"Error '{error_msg}' → {error_code}: {explanation}")
    
    return True

async def main():
    """Main test function that runs all tests."""
    print("Starting Starlink Crawler Package Tests")
    
    # Test sitemap parser
    urls = await test_sitemap_parser()
    
    # Test crawler
    await test_crawler(urls)
    
    # Test error handling
    await test_error_handling()
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    asyncio.run(main())
