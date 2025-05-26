# Starlink Crawler

A modular web crawler designed specifically for crawling and parsing Starlink-related documentation and websites. This package provides a flexible, configurable, and efficient way to extract content from sitemaps and save it as markdown files.

## Features

- **Parallel Crawling**: Efficiently crawl multiple URLs concurrently with configurable parallelism
- **Rate Limiting**: Built-in rate limiting to prevent overloading target servers
- **Memory Management**: Automatic memory usage monitoring to prevent crashes
- **Flexible Title Extraction**: Multiple strategies for extracting titles from content
- **Error Handling**: Comprehensive error tracking and explanation
- **Progress Tracking**: Detailed statistics during crawling operations
- **Configurable**: Extensive configuration options for customizing crawling behavior

## Installation

Clone the repository and navigate to the project directory:

```bash
git clone <repository-url>
cd starlink_crawler
```

## Usage

You can use the crawler either as a command-line tool or import it as a module in your Python code.

### Command-line Usage

Run the crawler from the command line:

```bash
python -m starlink_crawler.main
```

Follow the interactive prompts to configure and start the crawling process.

### Module Usage

Import and use the crawler in your Python code:

```python
import asyncio
from starlink_crawler.config import CrawlerConfig, TitleStrategy
from starlink_crawler.core import crawl_parallel_with_rate_limiting
from starlink_crawler.parsers import get_urls_from_source

async def example():
    # Get URLs from a sitemap
    urls = await get_urls_from_source('url', 'https://www.starlink.com/support/sitemap/en-US.xml')
    
    # Create a configuration
    config = CrawlerConfig(
        output_dir='./output',
        title_strategy=TitleStrategy.HEADING_FIRST,
        max_concurrent=5,
        request_rate=1.0
    )
    
    # Start crawling
    success, failed = await crawl_parallel_with_rate_limiting(urls, config)
    print(f"Crawling complete! Success: {success}, Failed: {failed}")

# Run the example
asyncio.run(example())
```

## Package Structure

The package is organized into the following modules:

- **config**: Configuration classes and settings
  - `crawler_config.py`: Main configuration class
  - `title_strategy.py`: Title extraction strategy enum
- **core**: Core crawling functionality
  - `crawler.py`: Main crawling function
  - `rate_limiting.py`: Rate limiting implementation
- **parsers**: Content parsing utilities
  - `sitemap_parser.py`: XML sitemap parsing
  - `title_extraction.py`: Title extraction from content
- **utils**: Utility functions and classes
  - `error_handling.py`: Error tracking and explanation
  - `stats.py`: Crawling statistics
  - `task_polling.py`: Async task polling
  - `url_processing.py`: URL processing and tracking

## Configuration Options

The `CrawlerConfig` class provides numerous options to customize the crawler's behavior:

- `max_concurrent`: Maximum number of concurrent requests
- `memory_threshold`: Memory usage threshold percentage
- `min_batch_delay`, `max_batch_delay`: Delay range between batches
- `dynamic_delay`: Whether to adjust delay based on error rates
- `request_rate`: Requests per second rate limit
- `burst`: Burst size for rate limiting
- `max_crawls_per_minute`: Maximum crawls per minute
- `output_dir`: Directory for markdown output files
- `title_strategy`: Strategy for extracting titles
- `skip_existing`: Whether to skip already processed URLs
- `task_poll_interval`: Interval between task polling attempts
- `max_task_polls`: Maximum number of task polling attempts

## Title Extraction Strategies

The crawler supports multiple strategies for extracting titles from content:

- `HEADING_FIRST`: First heading, then URL, then first line
- `URL_FIRST`: URL, then first heading, then first line
- `FIRST_LINE_FIRST`: First line, then first heading, then URL
- `HEADING_ONLY`: Only use first heading, fallback to empty
- `URL_ONLY`: Only use URL, no fallbacks

## License

[MIT License](LICENSE)
