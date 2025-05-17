import os
import sys
import time
import asyncio
import requests
from xml.etree import ElementTree
from typing import List
import random
from datetime import datetime

# Import crawler components from crawl4ai library
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

# Set up directory structure for input/output files
__location__ = os.path.dirname(os.path.abspath(__file__))     # Current script directory
# __input__ = os.path.join(__location__, "xml_input_files")     # Directory containing XML sitemaps
__output__ = os.path.join(__location__, "starlink_markdown_output_files")    # Directory for markdown output files
os.makedirs(__output__, exist_ok=True)

# Enable imports from parent directory for shared modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

class RateLimiter:
    """Simple token bucket rate limiter"""
    def __init__(self, rate: float, burst: int = 1):
        self.rate = rate  # tokens per second
        self.burst = burst  # max tokens
        self.tokens = burst  # current tokens
        self.last_update = time.time()
    
    async def acquire(self):
        """Acquire a token, waiting if necessary"""
        while self.tokens <= 0:
            now = time.time()
            time_passed = now - self.last_update
            self.tokens = min(self.burst, self.tokens + time_passed * self.rate)
            self.last_update = now
            if self.tokens <= 0:
                await asyncio.sleep(0.1)
        self.tokens -= 1

async def crawl_with_backoff(crawler, url, config, session_id, rate_limiter):
    """Crawl with exponential backoff on 429 errors"""
    max_retries = 5
    base_delay = 5.0
    
    for attempt in range(max_retries):
        # Wait for rate limiter
        await rate_limiter.acquire()
        
        # Attempt the crawl
        result = await crawler.arun(
            url=url,
            config=config,
            session_id=session_id
        )
        
        # Check if we hit a rate limit
        if result and "429" in str(result.error_message):
            delay = base_delay * (2 ** attempt)  # exponential backoff
            print(f"Rate limited. Waiting {delay:.1f}s before retry...")
            await asyncio.sleep(delay)
            continue
            
        return result
    
    return None

# Sequential crawling function
async def crawl_sequential(urls: List[str], batch_size: int = None, start_index: int = 0):
    """
    Sequentially crawl a list of URLs and save markdown output.
    
    Args:
        urls: List of URLs to crawl
        batch_size: Optional number of URLs to process in this batch
        start_index: Starting index for page numbering (default: 0)
    
    Returns:
        tuple: (success_count, fail_count) - Number of successful and failed crawls
    """
    # Print header
    print("\n=== Sequential Crawling with Rate Limiting ===")

    # Initialize browser
    browser_config = BrowserConfig(
        headless=True,
        verbose=False,
        # For better performance in Docker or low-memory environments:
        extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
    )

    # Initialize crawler
    crawl_config = CrawlerRunConfig(
        markdown_generator=DefaultMarkdownGenerator()
    )

    # Initialize rate limiter (1 request per 5 seconds, burst of 2)
    rate_limiter = RateLimiter(rate=0.2, burst=2)

    # Create the crawler (opens the browser)
    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()

    # Try to crawl URLs
    try:
        # Initialize counters and index
        success_count = 0
        fail_count = 0
        page_index = 1
        
        # Calculate target URLs for this batch
        target_urls = urls[:batch_size] if batch_size else urls
        total_batch = len(target_urls)
        
        # Process URLs in current batch
        for i, url in enumerate(target_urls, 1):
            current_index = start_index + i
            
            # Use crawl_with_backoff instead of direct crawler.arun
            result = await crawl_with_backoff(
                crawler=crawler,
                url=url,
                config=crawl_config,
                session_id=f"seq_session_{current_index}",
                rate_limiter=rate_limiter
            )
            
            # Handle successful crawls
            if result and result.success:
                success_count += 1
                
                # Print success message with batch progress
                print(f"[{i}/{total_batch}] Successfully crawled: {url}")
                
                # Check markdown length
                print(f"Markdown length: {len(result.markdown_v2.raw_markdown)}")

                # Save markdown to file
                output_file = os.path.join(__output__, f"page_{current_index}.md")
                
                # Write markdown content to file
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(result.markdown)
                print(f"✅ Saved: {output_file}")
            else:
                fail_count += 1
                error_msg = result.error_message if result else "No result"
                print(f"[{i}/{total_batch}] Failed: {url} - Error: {error_msg}")
            
            # Log current time and counts every 10 pages
            if i % 10 == 0:
                now = datetime.now().strftime("%H:%M:%S")
                print(f"\n[{now}] Batch progress: {i}/{total_batch} URLs")
                print(f"Success: {success_count}, Failed: {fail_count}\n")

        # Print summary
        print(f"\n📊 Summary:")
        print(f"  ✅ Successfully crawled and saved: {success_count}")
        print(f"  ❌ Failed to crawl: {fail_count}")
        
        return success_count, fail_count

    finally:
        # After all URLs are done, close the crawler (and the browser)
        await crawler.close()

def get_starlink_support_docs_urls():
    """
    Fetches all URLs from the sitemap.xml file to get the content.
    
    Returns:
        List[str]: List of URLs
    """
    
    # URL of the sitemap
    # Starlink
    sitemap_url = "https://www.starlink.com/support/sitemap/en-US.xml"
    # Zenduty
    # sitemap_url = "https://zenduty.com/docs/sitemap-posts.xml"
    # Peplink
    # sitemap_url = "https://forum.peplink.com/sitemap_1.xml"
    # sitemap_url = "https://forum.peplink.com/sitemap_2.xml"
    # sitemap_url = "https://forum.peplink.com/sitemap_3.xml"
    # Skydio
    # sitemap_url = "https://support.skydio.com/hc/sitemap.xml"
    
    print(f"\nFetching URLs from: {sitemap_url}")
    
    # Try to fetch and parse the sitemap
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        
        # Parse the XML
        root = ElementTree.fromstring(response.content)
        
        # Extract all URLs from the sitemap
        # The namespace is usually defined in the root element
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]
        
        # Filter out these pages
        # urls = [url for url in urls if url != "https://www.starlink.com/support"]
        
        return urls
        
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return []

async def main():
    """
    Main async entry point.
    - Fetches sitemap URLs.
    - Handles batch size selection.
    - Manages crawling process with batch control.
    """
    
    # Get URLs from sitemap
    urls = get_starlink_support_docs_urls()
    
    # If URLs are found, handle batch processing
    if urls:
        total_urls = len(urls)
        print(f"\nFound {total_urls} URLs to crawl")
        print("This may take a while for large numbers of URLs.")
        print("Each URL will be processed with rate limiting (1 request per 5 seconds).")
        
        # Ask for batch size
        while True:
            try:
                batch_input = input(f"\nHow many URLs would you like to process first? (1-{total_urls}, or press Enter for all): ")
                if not batch_input:
                    batch_size = None
                    break
                batch_size = int(batch_input)
                if 1 <= batch_size <= total_urls:
                    break
                print(f"Please enter a number between 1 and {total_urls}")
            except ValueError:
                print("Please enter a valid number")
        
        # Calculate and show processing time
        process_urls = batch_size if batch_size else total_urls
        process_time = (process_urls * 5) / 60
        print(f"Estimated minimum processing time: {process_time:.1f} minutes")
        
        # Ask for confirmation
        response = input(f"\nDo you want to proceed with crawling {process_urls} URLs? (y/n): ")
        if response.lower() != 'y':
            print("Operation cancelled by user.")
            return
        
        # Process first batch
        success, failed = await crawl_sequential(urls, batch_size)
        print(f"\nBatch complete! Success: {success}, Failed: {failed}")
        
        # If we processed a batch and there are more URLs, ask to continue
        if batch_size and batch_size < total_urls:
            remaining = total_urls - batch_size
            response = input(f"\nProcessed first {batch_size} URLs. Continue with remaining {remaining} URLs? (y/n): ")
            if response.lower() == 'y':
                more_success, more_failed = await crawl_sequential(urls[batch_size:], None, batch_size)
                print(f"\nAll processing complete!")
                print(f"Total Success: {success + more_success}")
                print(f"Total Failed: {failed + more_failed}")
            else:
                print("Crawling stopped after first batch.")
    
    # If no URLs are found, print a message
    else:
        print("No URLs found to crawl")

if __name__ == "__main__":
    asyncio.run(main())