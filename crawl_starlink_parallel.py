import os
import sys
import time
import asyncio
import psutil
import requests
import re
import hashlib
import json
import glob
from xml.etree import ElementTree
from typing import List, Dict, Any, Optional, Tuple, Set
import random
from datetime import datetime
from urllib.parse import urlparse

# Import crawler components from crawl4ai library
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

# Set up directory structure for input/output files
__location__ = os.path.dirname(os.path.abspath(__file__))     # Current script directory
__output__ = os.path.join(__location__, "starlink_markdown_output_files")    # Directory for markdown output files
os.makedirs(__output__, exist_ok=True)

# Enable imports from parent directory for shared modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

class TitleStrategy:
    """Enum-like class for title extraction strategies"""
    HEADING_FIRST = "heading_first"  # Try headings first, then first line, then URL
    URL_FIRST = "url_first"          # Try URL path first, then headings, then first line
    FIRST_LINE_FIRST = "first_line_first"  # Try first line first, then headings, then URL
    HEADING_ONLY = "heading_only"    # Only use headings, fall back to URL + timestamp
    URL_ONLY = "url_only"            # Only use URL path, fall back to domain + timestamp
    
    @staticmethod
    def get_description(strategy):
        descriptions = {
            TitleStrategy.HEADING_FIRST: "Extract from headings first, then first line, then URL",
            TitleStrategy.URL_FIRST: "Extract from URL path first, then headings, then first line",
            TitleStrategy.FIRST_LINE_FIRST: "Extract from first line first, then headings, then URL",
            TitleStrategy.HEADING_ONLY: "Only extract from headings (# or ## or ###)",
            TitleStrategy.URL_ONLY: "Only extract from URL path"
        }
        return descriptions.get(strategy, "Unknown strategy")

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
        output_dir: Optional[str] = None,     # Output directory for markdown files
        cache_mode: CacheMode = CacheMode.BYPASS,  # Cache mode
        title_strategy: str = TitleStrategy.HEADING_FIRST,  # Title extraction strategy
        skip_existing: bool = True            # Whether to skip already processed URLs
    ):
        self.max_concurrent = max_concurrent
        self.memory_threshold = memory_threshold
        self.min_batch_delay = min_batch_delay
        self.max_batch_delay = max_batch_delay
        self.dynamic_delay = dynamic_delay
        self.request_rate = request_rate
        self.burst = burst
        self.output_dir = output_dir
        self.cache_mode = cache_mode
        self.title_strategy = title_strategy
        self.skip_existing = skip_existing

        # Create output directory if specified
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

class ErrorInfo:
    """Stores information about HTTP and other errors"""
    # HTTP status code explanations
    HTTP_STATUS_CODES = {
        400: "Bad Request - The server cannot process the request due to a client error",
        401: "Unauthorized - Authentication is required and has failed or not been provided",
        403: "Forbidden - The server understood the request but refuses to authorize it",
        404: "Not Found - The requested resource could not be found",
        429: "Too Many Requests - Rate limiting has been applied",
        500: "Internal Server Error - The server has encountered a situation it doesn't know how to handle",
        502: "Bad Gateway - The server was acting as a gateway or proxy and received an invalid response",
        503: "Service Unavailable - The server is not ready to handle the request",
        504: "Gateway Timeout - The server is acting as a gateway and cannot get a response in time"
    }
    
    # Network error explanations
    NETWORK_ERRORS = {
        "ERR_CONNECTION_REFUSED": "Connection Refused - The target server refused the connection",
        "ERR_CONNECTION_RESET": "Connection Reset - The connection was reset during the operation",
        "ERR_CONNECTION_CLOSED": "Connection Closed - The connection was closed unexpectedly",
        "ERR_CONNECTION_TIMED_OUT": "Connection Timeout - The connection attempt timed out",
        "ERR_INTERNET_DISCONNECTED": "Internet Disconnected - No internet connection available",
        "ERR_NAME_NOT_RESOLVED": "DNS Error - The hostname could not be resolved",
        "ERR_ADDRESS_UNREACHABLE": "Address Unreachable - The IP address is unreachable",
        "ERR_FAILED": "General Failure - The operation failed for an unspecified reason",
        "ERR_HTTP_RESPONSE_CODE_FAILURE": "HTTP Response Code Failure - Received an error HTTP status code"
    }
    
    @staticmethod
    def get_error_explanation(error_message: str) -> Tuple[str, str]:
        """Extract error code and provide explanation from an error message"""
        # Check for HTTP status code
        http_match = re.search(r'status=([0-9]{3})', error_message)
        if http_match:
            status_code = int(http_match.group(1))
            explanation = ErrorInfo.HTTP_STATUS_CODES.get(
                status_code, 
                f"HTTP {status_code} - Unknown HTTP status code"
            )
            return f"HTTP {status_code}", explanation
        
        # Check for network errors
        for error_code, explanation in ErrorInfo.NETWORK_ERRORS.items():
            if error_code in error_message:
                return error_code, explanation
        
        # If no specific error found
        return "UNKNOWN_ERROR", "Unknown error - Could not determine the specific error type"

class CrawlStats:
    """Tracks crawling statistics"""
    def __init__(self):
        self.success_count = 0
        self.fail_count = 0
        self.skipped_count = 0  # Count of skipped URLs
        self.peak_memory = 0
        self.start_time = datetime.now()
        self.process = psutil.Process(os.getpid())
        self.errors = {}  # Dictionary to track errors by URL
        self.skipped = {}  # Dictionary to track skipped URLs

    def log_memory(self, prefix: str = "") -> None:
        """Log current and peak memory usage"""
        current_mem = self.process.memory_info().rss
        if current_mem > self.peak_memory:
            self.peak_memory = current_mem
        print(f"{prefix} Current Memory: {current_mem // (1024 * 1024)} MB, Peak: {self.peak_memory // (1024 * 1024)} MB")

    def print_summary(self) -> None:
        """Print crawl statistics summary"""
        duration = datetime.now() - self.start_time
        print(f"\n📊 Summary:")
        print(f"  ✅ Successfully crawled: {self.success_count}")
        print(f"  ❌ Failed: {self.fail_count}")
        print(f"  ⏭️ Skipped (already processed): {self.skipped_count}")
        print(f"  ⏱️ Duration: {duration}")
        print(f"  📈 Peak memory (MB): {self.peak_memory // (1024 * 1024)}")
        
        # Print error summary if there were errors
        if self.errors:
            print("\n❌ Error Summary:")
            error_types = {}
            
            # Count occurrences of each error type
            for url, (error_code, explanation) in self.errors.items():
                if error_code not in error_types:
                    error_types[error_code] = 0
                error_types[error_code] += 1
            
            # Print error type counts
            for error_code, count in error_types.items():
                print(f"  {error_code}: {count} occurrences")
                
            # Ask if user wants to see detailed errors
            show_details = input("\nShow detailed error list? (y/n): ").lower() == 'y'
            if show_details:
                print("\nDetailed Errors:")
                for url, (error_code, explanation) in self.errors.items():
                    print(f"  {url}\n    {error_code}: {explanation}\n")
                    
            # Ask if user wants to save errors to file
            save_errors = input("\nSave errors to file? (y/n): ").lower() == 'y'
            if save_errors:
                self.save_errors_to_file()
    
    def save_errors_to_file(self) -> None:
        """Save error information to a JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        error_file = f"crawl_errors_{timestamp}.json"
        
        # Convert errors dict to serializable format
        error_data = {
            "timestamp": timestamp,
            "total_success": self.success_count,
            "total_failed": self.fail_count,
            "errors": {url: {"error_code": code, "explanation": expl} 
                      for url, (code, expl) in self.errors.items()}
        }
        
        # Save to file
        try:
            with open(error_file, 'w', encoding='utf-8') as f:
                json.dump(error_data, f, indent=2)
            print(f"Errors saved to {error_file}")
        except Exception as e:
            print(f"Error saving to file: {e}")

class RateLimiter:
    """Simple token bucket rate limiter for pre-batch throttling"""
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

def get_processed_urls(output_dir: str) -> Tuple[Set[str], Set[str]]:
    """
    Get sets of URLs that have already been processed by examining existing files.
    Separates successfully processed URLs from error URLs that should be retried.
    
    Args:
        output_dir: Directory containing processed markdown files
        
    Returns:
        Tuple[Set[str], Set[str]]: (successfully processed URLs, error URLs)
    """
    success_urls = set()
    error_urls = set()
    
    # Skip if output directory doesn't exist
    if not os.path.exists(output_dir):
        return success_urls, error_urls
    
    # Get all markdown files in the output directory
    md_files = glob.glob(os.path.join(output_dir, "*.md"))
    
    # Extract URLs from file metadata
    for file_path in md_files:
        try:
            # Check if this is an error file
            is_error_file = os.path.basename(file_path).startswith("err-")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(500)  # Read just enough to get the metadata
                
                # Extract URL from metadata
                url_match = re.search(r'url:\s*"([^"]+)"', content)
                if url_match:
                    url = url_match.group(1)
                    if is_error_file:
                        error_urls.add(url)
                    else:
                        success_urls.add(url)
        except Exception:
            # Skip files that can't be read
            continue
    
    return success_urls, error_urls

async def crawl_parallel_with_rate_limiting(urls: List[str], config: CrawlerConfig, batch_size: int = None, start_index: int = 0):
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
    if config.output_dir:
        print(f"Output directory: {config.output_dir}")

    # Initialize browser
    browser_config = BrowserConfig(
        headless=True,
        verbose=False,
        # For better performance in Docker or low-memory environments:
        extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],
    )

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
            # Create tasks for each URL in the batch
            tasks = []
            for url in batch:
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
                if result and result.success and result.markdown:
                    stats.success_count += 1
                    
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
                    error_msg = result.error_message if result and hasattr(result, 'error_message') else "Unknown error"
                    
                    # Extract error code and explanation
                    error_code, explanation = ErrorInfo.get_error_explanation(str(error_msg))
                    
                    # Store error information
                    stats.errors[url] = (error_code, explanation)
                    
                    # Print error with code and brief explanation
                    print(f"❌ [{i + j + 1}/{total_batch}] Error crawling {url}")
                    print(f"   Error code: {error_code}")
                    print(f"   Explanation: {explanation}")
                    
                    # Save error information to file
                    if config.output_dir:
                        # Extract title from URL using the same strategy as successful crawls
                        normal_title = extract_title_from_markdown("", url, config.title_strategy)
                        
                        # Create error code prefix (e.g., "err-429_")
                        error_prefix = f"err-{error_code.replace('HTTP ', '').replace(' ', '-').lower()}_"
                        
                        # Combine for final title
                        title = normal_title
                        
                        # Generate a safe filename with error prefix
                        safe_title = generate_safe_filename(title, url, page_index)
                        # Insert error prefix before the extension
                        base, ext = os.path.splitext(safe_title)
                        filename = f"{error_prefix}{base}{ext}"
                        output_file = os.path.join(config.output_dir, filename)
                        
                        try:
                            with open(output_file, "w", encoding="utf-8") as f:
                                # Add metadata header
                                f.write(f"<!--\ntitle: \"Error: {error_code}\"\n")
                                f.write(f"url: \"{url}\"\n")
                                f.write(f"error_code: \"{error_code}\"\n")
                                f.write(f"error_explanation: \"{explanation}\"\n-->\n\n")
                                
                                # Write error information as markdown content
                                f.write(f"# Error: {error_code}\n\n")
                                f.write(f"## URL\n{url}\n\n")
                                f.write(f"## Explanation\n{explanation}\n\n")
                                f.write(f"## Error Details\n```\n{error_msg}\n```\n")
                                
                            print(f"   Saved error information to: {output_file}")
                            page_index += 1
                        except Exception as e:
                            print(f"   Error saving error information: {e}")
            
            # Add dynamic delay between batches if not the last batch
            if i + config.max_concurrent < len(target_urls):
                # Calculate delay based on configuration
                if config.dynamic_delay:
                    # Use dynamic delay with exponential backoff based on error rate
                    error_rate = stats.fail_count / (stats.success_count + stats.fail_count + 0.001)
                    
                    # Increase delay as error rate increases
                    base_delay = config.min_batch_delay + (error_rate * 2 * (config.max_batch_delay - config.min_batch_delay))
                    
                    # Add randomness to avoid detection patterns (±20%)
                    jitter = random.uniform(0.8, 1.2)
                    delay = base_delay * jitter
                    
                    # Ensure delay is within configured bounds
                    delay = max(config.min_batch_delay, min(config.max_batch_delay, delay))
                else:
                    # Use fixed delay with small jitter
                    delay = config.min_batch_delay
                
                # Round to 1 decimal place for display
                display_delay = round(delay, 1)
                print(f"Waiting {display_delay}s before next batch...")
                
                # Apply the delay
                await asyncio.sleep(delay)
                
    except Exception as e:
        print(f"❌ Critical error during crawling: {e}")
        raise
    finally:
        # Close the crawler
        await crawler.stop()
        
        # Print summary
        stats.print_summary()
    
    return stats.success_count, stats.fail_count

def extract_title_from_markdown(markdown_content, url, strategy=TitleStrategy.HEADING_FIRST):
    """
    Extract a title from markdown content or generate one from the URL based on the selected strategy.
    
    Args:
        markdown_content: The markdown content to extract title from
        url: The URL of the page, used as fallback for title generation
        strategy: The title extraction strategy to use
        
    Returns:
        str: Extracted or generated title
    """
    # Define extraction functions for each method
    def extract_from_heading():
        if not markdown_content:
            return None
        # Look for the first heading (# or ## or ###)
        heading_pattern = re.compile(r'^(#{1,3})\s+(.+)$', re.MULTILINE)
        match = heading_pattern.search(markdown_content)
        if match:
            return match.group(2).strip()
        return None
    
    def extract_from_first_line():
        if not markdown_content:
            return None
        # Look for the first line with content
        lines = markdown_content.split('\n')
        for line in lines:
            if line.strip() and not line.startswith('<!--') and not line.startswith('-->'):  
                # Use first 50 chars as title if it's reasonably long
                if len(line.strip()) > 10:
                    return line.strip()[:50] + ('...' if len(line.strip()) > 50 else '')
        return None
    
    def extract_from_url_path():
        parsed_url = urlparse(url)
        path_parts = [p for p in parsed_url.path.split('/') if p]
        
        # Try to get a meaningful title from path
        if path_parts:
            # Use the last path segment, replacing hyphens and underscores with spaces
            path_title = path_parts[-1].replace('-', ' ').replace('_', ' ')
            # Remove file extensions if present
            path_title = re.sub(r'\.[a-zA-Z0-9]+$', '', path_title)
            if path_title:
                return path_title.title()
        return None
    
    def get_fallback_title():
        # If all else fails, use domain + timestamp
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"Content from {domain} ({timestamp})"
    
    # Apply strategies in different orders based on the selected strategy
    if strategy == TitleStrategy.HEADING_FIRST:
        return extract_from_heading() or extract_from_first_line() or extract_from_url_path() or get_fallback_title()
    
    elif strategy == TitleStrategy.URL_FIRST:
        return extract_from_url_path() or extract_from_heading() or extract_from_first_line() or get_fallback_title()
    
    elif strategy == TitleStrategy.FIRST_LINE_FIRST:
        return extract_from_first_line() or extract_from_heading() or extract_from_url_path() or get_fallback_title()
    
    elif strategy == TitleStrategy.HEADING_ONLY:
        return extract_from_heading() or get_fallback_title()
    
    elif strategy == TitleStrategy.URL_ONLY:
        return extract_from_url_path() or get_fallback_title()
    
    # Default fallback
    return get_fallback_title()

def generate_safe_filename(title, url, index):
    """
    Generate a safe filename from title and URL.
    
    Args:
        title: The title to use for the filename
        url: The URL of the page, used as fallback
        index: Current page index for uniqueness
        
    Returns:
        str: Safe filename ending with .md
    """
    # Remove invalid filename characters and limit length
    safe_title = re.sub(r'[^\w\s-]', '', title).strip()
    safe_title = re.sub(r'[-\s]+', '-', safe_title)
    
    # If title is too short or empty, use URL hash
    if len(safe_title) < 5:
        # Create a hash from the URL for uniqueness
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        safe_title = f"page-{url_hash}"
    
    # Limit filename length and ensure uniqueness with index
    safe_title = safe_title[:50]
    return f"{safe_title}-{index}.md"

async def parse_xml_file(file_path):
    """
    Parse a local XML sitemap file to extract URLs.
    
    Args:
        file_path: Path to the XML file
        
    Returns:
        List[str]: List of URLs extracted from the XML file
    """
    print(f"\nParsing XML file: {file_path}")
    
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"Error: XML file not found at {file_path}")
            return []
            
        # Read and parse the XML file
        with open(file_path, 'r', encoding='utf-8') as f:
            xml_content = f.read()
            
        # Parse the XML
        root = ElementTree.fromstring(xml_content)
        
        # Extract all URLs from the sitemap
        # The namespace is usually defined in the root element
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]
        
        return urls
        
    except Exception as e:
        print(f"Error parsing XML file: {e}")
        return []

async def get_urls_from_source(source_type, source_path):
    """
    Get URLs from either a sitemap URL or a local XML file.
    
    Args:
        source_type: Type of source ('url' or 'file')
        source_path: URL or file path to the sitemap
        
    Returns:
        List[str]: List of URLs
    """
    if source_type == 'url':
        # URL of the sitemap
        print(f"\nFetching URLs from: {source_path}")
        
        # Try to fetch and parse the sitemap
        try:
            response = requests.get(source_path)
            response.raise_for_status()
            
            # Parse the XML
            root = ElementTree.fromstring(response.content)
            
            # Extract all URLs from the sitemap
            # The namespace is usually defined in the root element
            namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]
            
            return urls
            
        except Exception as e:
            print(f"Error fetching sitemap: {e}")
            return []
    elif source_type == 'file':
        return await parse_xml_file(source_path)
    else:
        print(f"Unsupported source type: {source_type}")
        return []

async def main():
    """
    Main async entry point.
    - Fetches sitemap URLs from URL or local file.
    - Handles batch size selection.
    - Manages crawling process with batch control.
    """
    
    # Ask for input source type
    while True:
        source_type = input("\nEnter source type (url/file): ").lower()
        if source_type in ['url', 'file']:
            break
        print("Please enter either 'url' or 'file'")
    
    # Ask for source path based on type
    if source_type == 'url':
        # Provide default options
        sitemap_options = {
            '1': "https://www.starlink.com/support/sitemap/en-US.xml",
            # https://starlink-enterprise-guide.readme.io/
            '2': "https://zenduty.com/docs/sitemap-posts.xml",
            '3': "https://forum.peplink.com/sitemap_1.xml",
            '4': "https://support.skydio.com/hc/sitemap.xml"
        }
        
        print("\nAvailable sitemap URLs:")
        for key, url in sitemap_options.items():
            print(f"{key}: {url}")
        print("5: Enter custom URL")
        
        choice = input("Select an option (1-5): ")
        if choice in sitemap_options:
            source_path = sitemap_options[choice]
        else:
            source_path = input("Enter sitemap URL: ")
    else:
        # Ask for file path
        print("Enter path to XML sitemap file:")
        print("(e.g., ~/Documents/sitemap.xml)")
        source_path = input("> ")
        # Expand user directory if needed
        source_path = os.path.expanduser(source_path)
    
    # Get URLs from the selected source
    urls = await get_urls_from_source(source_type, source_path)
    
    # If URLs are found, handle batch processing
    if urls:
        total_urls = len(urls)
        print(f"\nFound {total_urls} URLs to crawl")
        print("This may take a while for large numbers of URLs.")
        
        # Set default configuration values
        default_config = {
            "batch_size": None,  # Process all URLs
            "max_concurrent": 5,  # 5 concurrent crawlers
            "request_rate": 0.2,  # 1 request per 5 seconds
            "dynamic_delay": True,  # Use dynamic delays
            "min_delay": 2.0,  # 2 seconds minimum delay
            "max_delay": 5.0,  # 5 seconds maximum delay
            "title_strategy": TitleStrategy.HEADING_FIRST,  # Extract from headings first
            "skip_existing": True  # Skip already processed URLs
        }
        
        # Define strategies list for reference
        strategies = [
            TitleStrategy.HEADING_FIRST,
            TitleStrategy.URL_FIRST,
            TitleStrategy.FIRST_LINE_FIRST,
            TitleStrategy.HEADING_ONLY,
            TitleStrategy.URL_ONLY
        ]
        
        # Display default configuration
        print("\n=== Default Configuration ===")
        print(f"Batch size: {'All URLs' if default_config['batch_size'] is None else default_config['batch_size']}")
        print(f"Max concurrent crawlers: {default_config['max_concurrent']}")
        print(f"Request rate: {default_config['request_rate']} requests/second")
        print(f"Delay strategy: {'Dynamic' if default_config['dynamic_delay'] else 'Fixed'}")
        print(f"Delay range: {default_config['min_delay']}-{default_config['max_delay']} seconds")
        print(f"Title strategy: {TitleStrategy.get_description(default_config['title_strategy'])}")
        print(f"Skip existing: {'Yes (only successful files)' if default_config['skip_existing'] else 'No'}")
        
        # Ask if user wants to use defaults or customize
        customize = input("\nUse these default settings? (y/n, default: y): ").lower() == 'n'
        
        # Initialize with defaults
        batch_size = default_config['batch_size']
        max_concurrent = default_config['max_concurrent']
        request_rate = default_config['request_rate']
        dynamic_delay = default_config['dynamic_delay']
        min_delay = default_config['min_delay']
        max_delay = default_config['max_delay']
        title_strategy = default_config['title_strategy']
        skip_existing = default_config['skip_existing']
        
        # If user wants to customize, prompt for each setting
        if customize:
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
            
            # Ask for crawl configuration
            try:
                max_input = input(f"\nMax concurrent crawlers (1-10, default: {max_concurrent}): ")
                if max_input:
                    max_concurrent = max(1, min(10, int(max_input)))
            except ValueError:
                pass
                
            try:
                rate_input = input(f"\nRequests per second per crawler (0.1-2.0, default: {request_rate}): ")
                if rate_input:
                    request_rate = max(0.1, min(2.0, float(rate_input)))
            except ValueError:
                pass
                
            # Ask for batch delay configuration
            print("\nBatch delay configuration:")
            print("1: Use dynamic delays (varies between min and max based on error rate)")
            print("2: Use fixed delay (constant delay between batches)")
            
            delay_choice = input(f"Select option (1-2, default: {1 if dynamic_delay else 2}): ")
            if delay_choice == "1":
                dynamic_delay = True
            elif delay_choice == "2":
                dynamic_delay = False
                
            try:
                if dynamic_delay:
                    min_input = input(f"\nMinimum delay between batches (1.0-10.0 seconds, default: {min_delay}): ")
                    if min_input:
                        min_delay = max(1.0, min(10.0, float(min_input)))
                        
                    max_input = input(f"Maximum delay between batches (must be >= {min_delay}, default: {max_delay}): ")
                    if max_input:
                        max_delay = max(min_delay, float(max_input))
                else:
                    delay_input = input(f"\nDelay between batches (1.0-10.0 seconds, default: {min_delay}): ")
                    if delay_input:
                        min_delay = max(1.0, min(10.0, float(delay_input)))
                        max_delay = min_delay  # Set max equal to min for fixed delay
            except ValueError:
                pass
                
            # Ask for title extraction strategy
            print("\nSelect title extraction strategy:")
            for i, strategy in enumerate(strategies, 1):
                print(f"{i}: {TitleStrategy.get_description(strategy)}")
                
            try:
                current_index = strategies.index(title_strategy) + 1
                strategy_input = input(f"Select strategy (1-{len(strategies)}, default: {current_index}): ")
                if strategy_input and 1 <= int(strategy_input) <= len(strategies):
                    title_strategy = strategies[int(strategy_input) - 1]
            except (ValueError, IndexError):
                pass
                
            # Ask whether to skip existing files
            skip_input = input(f"\nSkip successfully processed URLs? (y/n, default: {'y' if skip_existing else 'n'}): ").lower()
            if skip_input in ['y', 'n']:
                skip_existing = (skip_input == 'y')
            
        # Create crawler configuration
        config = CrawlerConfig(
            max_concurrent=max_concurrent,
            memory_threshold=70.0,
            min_batch_delay=min_delay,
            max_batch_delay=max_delay,
            dynamic_delay=dynamic_delay,
            request_rate=request_rate,
            burst=2,
            output_dir=__output__,
            title_strategy=title_strategy,
            skip_existing=skip_existing
        )
        
        # Calculate and show processing time (approximate)
        process_urls = batch_size if batch_size else total_urls
        # Estimate time based on number of batches and rate limiting
        num_batches = (process_urls + config.max_concurrent - 1) // config.max_concurrent
        process_time = (num_batches * (1/config.request_rate + config.batch_delay)) / 60
        print(f"Estimated minimum processing time: {process_time:.1f} minutes")
        
        # Ask for confirmation
        response = input(f"\nDo you want to proceed with crawling {process_urls} URLs? (y/n): ")
        if response.lower() != 'y':
            print("Operation cancelled by user.")
            return
        
        # Process first batch
        success, failed = await crawl_parallel_with_rate_limiting(urls, config, batch_size)
        print(f"\nBatch complete! Success: {success}, Failed: {failed}")
        
        # If we processed a batch and there are more URLs, ask to continue
        if batch_size and batch_size < total_urls:
            remaining = total_urls - batch_size
            response = input(f"\nProcessed first {batch_size} URLs. Continue with remaining {remaining} URLs? (y/n): ")
            if response.lower() == 'y':
                more_success, more_failed = await crawl_parallel_with_rate_limiting(urls[batch_size:], config, None, batch_size)
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
