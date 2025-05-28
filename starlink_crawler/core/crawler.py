"""
Core crawler functionality for the Starlink crawler.
This module provides the main crawling logic with memory-adaptive dispatching and rate limiting.
"""

import os
import json
import time
import random
import asyncio
from typing import List, Tuple, Set, Dict, Any

# Import from crawl4ai library
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

# Import from our package
from starlink_crawler.config import CrawlerConfig, TitleStrategy
from starlink_crawler.core.rate_limiting import RateLimiter
from starlink_crawler.utils.error_handling import ErrorInfo
from starlink_crawler.utils.stats import CrawlStats
from starlink_crawler.utils.task_polling import poll_task_result, is_task_id_response
from starlink_crawler.utils.url_processing import get_processed_urls
from starlink_crawler.parsers.title_extraction import extract_title_from_markdown, generate_safe_filename

async def crawl_parallel_with_rate_limiting(urls: List[str], config: CrawlerConfig, batch_size: int = None, start_index: int = 0) -> Tuple[int, int]:
    """
    Parallel crawling with memory-adaptive dispatching and rate limiting.
    
    Args:
        urls: List of URLs to crawl
        config: CrawlerConfig instance with crawler settings
        batch_size: Optional number of URLs to process in this batch
        start_index: Starting index for page numbering (default: 0)
    
    Returns:
        tuple: (success_count, fail_count) - Number of successful and failed crawls
    """
    # Initialize statistics tracker
    stats = CrawlStats()
    
    # Print header
    print("\n=== Parallel Crawling with Memory Management and Rate Limiting ===")
    print(f"URLs to process: {len(urls) if batch_size is None else min(len(urls), batch_size)}")
    print(f"Max concurrent: {config.max_concurrent}")
    print(f"Memory threshold: {config.memory_threshold}%")
    print(f"Rate limiting: {config.request_rate} requests/second (burst: {config.burst})")
    if config.max_crawls_per_minute > 0:
        print(f"Max crawls per minute: {config.max_crawls_per_minute}")
    if config.delay_type == "fixed":
        print(f"Batch delay: {config.min_batch_delay}s (fixed)")
    else:
        print(f"Batch delay range: {config.min_batch_delay}-{config.max_batch_delay}s (randomized)")
    if config.output_dir:
        print(f"Output directory: {config.output_dir}")

    # Initialize browser
    browser_config = BrowserConfig(
        headless=True,
        verbose=False,
        # For better performance in Docker or low-memory environments:
        extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
    )
    
    # Print delay type and request delay settings
    print(f"Delay type: {'Fixed' if config.delay_type == 'fixed' else 'Random'}")
    print(f"Request delays: {config.min_request_delay}-{config.max_request_delay}s between requests in a batch")

    # Initialize crawler
    crawl_config = CrawlerRunConfig(
        markdown_generator=DefaultMarkdownGenerator(),
        cache_mode=config.cache_mode
    )

    # Initialize rate limiter for batch throttling
    rate_limiter = RateLimiter(rate=config.request_rate * config.max_concurrent, burst=config.burst)

    # Track memory usage for adaptive concurrency
    # We'll manage concurrency manually instead of using MemoryAdaptiveDispatcher

    # Get already processed URLs if needed
    success_urls = set()
    error_urls = set()
    if config.skip_existing and config.output_dir:
        success_urls, error_urls = get_processed_urls(config.output_dir)
        if success_urls:
            print(f"Found {len(success_urls)} successfully processed URLs that will be skipped")
        if error_urls:
            print(f"Found {len(error_urls)} previously failed URLs that will be retried")
    
    # Filter out successfully processed URLs if skip_existing is enabled
    if config.skip_existing and success_urls:
        original_urls = urls.copy()
        urls = [url for url in urls if url not in success_urls]
        skipped_urls = [url for url in original_urls if url in success_urls]
        
        # Store skipped URLs in stats
        for url in skipped_urls:
            stats.skipped[url] = "Already processed successfully"
        stats.skipped_count = len(skipped_urls)
        
        # Print skipped count
        if stats.skipped_count > 0:
            print(f"Skipping {stats.skipped_count} successfully processed URLs")
            
        # Print retry count
        retry_count = sum(1 for url in urls if url in error_urls)
        if retry_count > 0:
            print(f"Will retry {retry_count} previously failed URLs")
    
    # Calculate target URLs for this batch
    target_urls = urls[:batch_size] if batch_size else urls
    total_batch = len(target_urls)
    
    # Page index counter
    page_index = start_index + 1

    # Create the crawler (opens the browser)
    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()

    # Try to crawl URLs
    try:
        # Process URLs in batches based on max_concurrent setting
        for i in range(0, len(target_urls), config.max_concurrent):
            # Wait for rate limiter before starting a new batch
            await rate_limiter.acquire()
            
            # Get current batch of URLs
            batch = target_urls[i:i + config.max_concurrent]
            batch_num = i // config.max_concurrent + 1
            
            print(f"\nProcessing batch {batch_num}/{(len(target_urls) + config.max_concurrent - 1) // config.max_concurrent}")
            for j, url in enumerate(batch):
                print(f"  [{i + j + 1}/{total_batch}] {url}")
            
            # Log memory before batch
            stats.log_memory(f"Before batch {batch_num}: ")
            
            # Process the batch in parallel with manual concurrency management
            # Create tasks for each URL in the batch with small delays between them
            tasks = []
            for url in batch:
                # Add a small random delay between requests (except for the first one)
                if len(tasks) > 0 and config.min_request_delay > 0:
                    # Use a random delay between min and max request delay
                    delay = random.uniform(config.min_request_delay, config.max_request_delay)
                    print(f"  Adding {delay:.2f}s delay before requesting {url}")
                    await asyncio.sleep(delay)
                
                # Create a task for each URL
                task = crawler.arun(
                    url=url,
                    config=crawl_config,
                    session_id=f"session_{i + batch.index(url) + 1}"
                )
                tasks.append(task)
                
            # Run all tasks concurrently and gather results
            batch_results = await asyncio.gather(*tasks)
            
            # Log memory after batch
            stats.log_memory(f"After batch {batch_num}: ")
            
            # Process batch results
            for j, (url, result) in enumerate(zip(batch, batch_results)):
                # Check if the result is a task ID that needs polling
                if result and isinstance(result, str) and await is_task_id_response(result):
                    print(f"Received task ID for {url}, polling for result...")
                    # Poll for the actual result
                    polled_result = await poll_task_result(crawler, result, config)
                    if polled_result:
                        result = polled_result
                    else:
                        # If polling failed, mark as error
                        stats.fail_count += 1
                        error_msg = "Task polling timed out after maximum attempts"
                        stats.errors[url] = error_msg
                        print(f"❌ Failed: {url} - TASK_TIMEOUT")
                        continue
                
                if result and result.success and result.markdown:
                    stats.success_count += 1
                    # Record timestamp for rate limiting
                    stats.crawl_timestamps.append(time.time())
                    
                    # Save to file if output directory specified
                    if config.output_dir:
                        # Extract title from markdown or generate from URL using selected strategy
                        title = extract_title_from_markdown(result.markdown, url, config.title_strategy)
                        
                        # Generate a safe filename
                        filename = generate_safe_filename(title, url, page_index)
                        output_file = os.path.join(config.output_dir, filename)
                        
                        try:
                            with open(output_file, "w", encoding="utf-8") as f:
                                # Add metadata header
                                f.write(f"<!--\ntitle: \"{title}\"\n")
                                f.write(f"url: \"{url}\"\n-->\n\n")
                                f.write(result.markdown)
                            print(f"✅ [{i + j + 1}/{total_batch}] Saved: {output_file}")
                            page_index += 1
                        except Exception as e:
                            print(f"❌ Error saving {output_file}: {e}")
                else:
                    stats.fail_count += 1
                    error_msg = str(result.error) if result.error else "Unknown error"
                    stats.errors[url] = error_msg
                    
                    # Extract error code
                    error_code = ErrorInfo.get_error_code(error_msg)
                    error_code_lower = error_code.lower() if error_code else ""
                    
                    # Extract HTTP status code and headers if available
                    status_code, headers = ErrorInfo.extract_response_details(error_msg)
                    
                    # Get explanation for the error
                    explanation = ErrorInfo.get_explanation(error_code, error_msg)
                    
                    # Log detailed error information
                    if status_code:
                        print(f"❌ Failed: {url} - {error_code} (HTTP Status: {status_code})")
                    else:
                        print(f"❌ Failed: {url} - {error_code}")
                    
                    # Save error information if output directory specified
                    if config.output_dir:
                        # Extract title from URL using the same strategy as successful crawls
                        normal_title = extract_title_from_markdown("", url, config.title_strategy)
                        
                        # Create error code prefix (e.g., "err-429_")
                        error_prefix = f"err-{error_code.replace('HTTP ', '').replace(' ', '-').lower()}_"
                        
                        # Combine for final title
                        title = normal_title
                        
                        # Generate a safe filename with error prefix
                        filename = error_prefix + generate_safe_filename(title, url, page_index)
                        output_file = os.path.join(config.output_dir, filename)
                        
                        try:
                            # Write error information to file
                            with open(output_file, 'w', encoding='utf-8') as f:
                                # Add metadata
                                f.write(f"<!--\n")
                                f.write(f"url: \"{url}\"\n")
                                f.write(f"error_code: \"{error_code}\"\n")
                                f.write(f"error_explanation: \"{explanation}\"\n")
                                if status_code:
                                    f.write(f"http_status_code: \"{status_code}\"\n")
                                f.write(f"-->\n\n")
                                
                                # Add error information
                                f.write(f"# Error: {error_code}\n\n")
                                f.write(f"## URL\n{url}\n\n")
                                f.write(f"## Explanation\n{explanation}\n\n")
                                
                                # Add HTTP status code if available
                                if status_code:
                                    f.write(f"## HTTP Status Code\n{status_code}\n\n")
                                
                                # Add headers if available
                                if headers:
                                    f.write(f"## Response Headers\n```json\n{json.dumps(headers, indent=2)}\n```\n\n")
                                
                                f.write(f"## Error Details\n```\n{error_msg}\n```\n")
                                
                            print(f"   Saved error information to: {output_file}")
                            page_index += 1
                        except Exception as e:
                            print(f"   Error saving error information: {e}")
            
            # Add delay between batches if not the last batch
            if i + config.max_concurrent < len(target_urls):
                # Apply delay based on delay type
                if config.delay_type == "fixed":
                    # Use fixed delay (min_batch_delay)
                    delay = config.min_batch_delay
                    print(f"Using fixed delay: {delay:.2f}s")
                else:  # random delay
                    # Use random delay between min and max
                    delay = random.uniform(config.min_batch_delay, config.max_batch_delay)
                    print(f"Using random delay: {delay:.2f}s")
                
                # Check if we need to wait longer to comply with max_crawls_per_minute
                if config.max_crawls_per_minute > 0 and stats.crawl_timestamps:
                    # Remove timestamps older than 1 minute
                    current_time = time.time()
                    stats.crawl_timestamps = [ts for ts in stats.crawl_timestamps if current_time - ts < 60]
                    
                    # Calculate crawls in the last minute
                    crawls_last_minute = len(stats.crawl_timestamps)
                    
                    # Calculate how many more crawls we can do in this batch
                    available_slots = config.max_crawls_per_minute - crawls_last_minute
                    
                    # If we're approaching the limit, add extra delay
                    if available_slots < len(batch):
                        # Calculate how long to wait for slots to free up
                        if available_slots <= 0:
                            # No slots available, wait until oldest timestamp is more than a minute ago
                            wait_time = 60 - (current_time - stats.crawl_timestamps[0])
                            print(f"⏱️ Rate limit reached ({crawls_last_minute}/{config.max_crawls_per_minute} per minute), waiting {wait_time:.2f}s for slots to free up")
                            delay = max(delay, wait_time)
                        else:
                            # Some slots available, but not enough for the whole batch
                            # Add delay to spread the remaining requests over the minute
                            spread_delay = 60 / config.max_crawls_per_minute * (len(batch) - available_slots)
                            print(f"⏱️ Approaching rate limit ({crawls_last_minute}/{config.max_crawls_per_minute} per minute), adding {spread_delay:.2f}s delay")
                            delay = max(delay, spread_delay)
                    
                # Wait before next batch
                display_delay = round(delay, 1)
                print(f"Waiting {display_delay}s before next batch...")
                
                # Apply the delay
                await asyncio.sleep(delay)
                
    except Exception as e:
        print(f"❌ Critical error during crawling: {e}")
        raise
    finally:
        # Print the summary
        stats.print_summary()
    
    return stats.success_count, stats.fail_count