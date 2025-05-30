# Starlink Crawler

A modular web crawler designed specifically for crawling and parsing Starlink-related documentation and websites. This package provides a flexible, configurable, and efficient way to extract content from sitemaps and save it as markdown files.

## Features

- **Parallel Crawling**: Efficiently crawl multiple URLs concurrently with configurable parallelism
- **Rate Limiting**: Built-in rate limiting with multiple strategies to prevent overloading target servers and avoid bot detection
- **Memory Management**: Automatic memory usage monitoring to prevent crashes
- **Flexible Title Extraction**: Multiple strategies for extracting titles from content
- **Error Handling**: Comprehensive error tracking and explanation
- **Progress Tracking**: Detailed statistics during crawling operations
- **Configurable**: Extensive configuration options for customizing crawling behavior
- **Configuration Persistence**: Save your preferred settings between sessions
- **Bot Detection Avoidance**: Staggered request patterns to appear more human-like
- **Markdown Cleaning**: Integrated and standalone options for cleaning and formatting markdown content

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
  - `config_persistence.py`: Configuration saving and loading
- **core**: Core crawling functionality
  - `crawler.py`: Main crawling function
  - `rate_limiting.py`: Rate limiting implementation
- **parsers**: Content parsing utilities
  - `sitemap_parser.py`: XML sitemap parsing
  - `title_extraction.py`: Title extraction from content
- **processors**: Content processing utilities
  - `markdown_cleaner.py`: Markdown cleaning and formatting
- **utils**: Utility functions and classes
  - `error_handling.py`: Error tracking and explanation
  - `stats.py`: Crawling statistics
  - `task_polling.py`: Async task polling
  - `url_processing.py`: URL processing and tracking

## Configuration Options

The `CrawlerConfig` class provides numerous options to customize the crawler's behavior:

- `max_concurrent`: Maximum number of concurrent requests
- `memory_threshold`: Memory usage threshold percentage
- `min_batch_delay`, `max_batch_delay`: Delay values between batches
- `delay_type`: Type of delay between batches ("fixed" or "random")
- `min_request_delay`, `max_request_delay`: Delay values between individual requests in a batch
- `request_rate`: Requests per second rate limit
- `burst`: Burst size for rate limiting
- `max_crawls_per_minute`: Maximum crawls per minute
- `output_dir`: Directory for markdown output files
- `title_strategy`: Strategy for extracting titles
- `skip_existing`: Whether to skip already processed URLs
- `task_poll_interval`: Interval between task polling attempts
- `max_task_polls`: Maximum number of task polling attempts
- `clean_markdown`: Whether to clean markdown during crawl
- `clean_output_dir`: Output directory for cleaned markdown
- `extract_metadata`: Whether to extract metadata from content
- `fix_urls`: Whether to fix malformed URLs
- `remove_navigation`: Whether to remove navigation elements
- `remove_footer`: Whether to remove footer content
- `add_frontmatter`: Whether to add YAML frontmatter

## Configuration Persistence

The crawler can save your configuration preferences between sessions:

- Automatically loads saved settings on startup
- Offers to save your current configuration before starting a crawl
- Stores settings in `~/.starlink_crawler_config.json`

This means you don't have to reconfigure your preferred settings each time you run the crawler.

## Bot Detection Avoidance

To reduce the risk of triggering bot detection systems, the crawler implements:

1. **Batch Delays**: Configurable delays between batches of requests
   - Fixed delay: Uses the same delay between each batch
   - Random delay: Randomly selects a delay between min and max values

2. **Per-Request Delays**: Small random delays between individual requests in a batch
   - Makes request patterns appear more human-like
   - Staggered requests instead of simultaneous bursts
   - Fully configurable min/max delay values

## Title Extraction Strategies

The crawler supports multiple strategies for extracting titles from content:

- `HEADING_FIRST`: First heading, then URL, then first line
- `URL_FIRST`: URL, then first heading, then first line
- `FIRST_LINE_FIRST`: First line, then first heading, then URL
- `HEADING_ONLY`: Only use first heading, fallback to empty
- `URL_ONLY`: Only use URL, no fallbacks

## Markdown Cleaning

The crawler includes powerful markdown cleaning capabilities that can be used in two ways:

### 1. Integrated Cleaning During Crawling

Enable markdown cleaning as part of the crawling process by setting the `clean_markdown` option to `True` in your configuration:

```python
config = CrawlerConfig(
    output_dir='./output',
    clean_markdown=True,
    clean_output_dir='./cleaned_output',  # Optional, defaults to output_dir
    extract_metadata=True,
    fix_urls=True,
    remove_navigation=True,
    remove_footer=True,
    add_frontmatter=True
)
```

This will:
1. Save the original markdown to the `output_dir`
2. Process and clean the markdown
3. Save the cleaned version to the `clean_output_dir` with improved formatting

### 2. Standalone Post-Processing with UI

Clean existing markdown files using the interactive UI or command-line tool:

```bash
# Interactive UI
python -m starlink_crawler.main_cleaner

# Command-line with options
python -m starlink_crawler.clean_markdown_ui [options]
```

The interactive UI provides a user-friendly interface to:
- View and modify all cleaning configuration options
- Preview files to be processed
- Save your preferred settings for future use
- Monitor progress during processing

Command-line options:
- `--input-dir`: Input directory containing markdown files to process
- `--output-dir`: Output directory for processed files
- `--no-metadata`: Skip metadata extraction
- `--no-fix-urls`: Skip URL fixing
- `--keep-navigation`: Keep navigation elements
- `--keep-footer`: Keep footer content
- `--no-frontmatter`: Skip adding YAML frontmatter
- `--language`: Content language (default: en)
- `--batch`: Process all files without confirmation (non-interactive mode)

Examples:

```bash
# Start the interactive UI
python -m starlink_crawler.main_cleaner

# Process files with specific options
python -m starlink_crawler.clean_markdown_ui --input-dir input_markdown --output-dir cleaned_output

# Process all files in batch mode (no interaction)
python -m starlink_crawler.clean_markdown_ui --input-dir input_markdown --output-dir cleaned_output --batch
```

### Cleaning Features

The markdown cleaner performs several important functions:

1. **Metadata Extraction**: Extracts title, URL, article ID, and category
2. **Content Cleaning**: Removes navigation elements and duplicate content
3. **URL Fixing**: Fixes malformed URLs and link formatting
4. **Footer Removal**: Removes unnecessary footer content
5. **YAML Frontmatter**: Creates standardized metadata headers
6. **File Renaming**: Uses article IDs for consistent file naming

## License

[MIT License](LICENSE)
