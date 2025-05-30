# Starlink Crawler Tasks

## Completed Tasks

### Modularization
- [x] Create basic package structure with directories and `__init__.py` files
- [x] Extract `TitleStrategy` class to `config/title_strategy.py`
- [x] Extract `CrawlerConfig` class to `config/crawler_config.py`
- [x] Extract `ErrorInfo` class to `utils/error_handling.py`
- [x] Extract `CrawlStats` class to `utils/stats.py`
- [x] Set up proper imports in package `__init__.py` files

### Enhancements
- [x] Simplify batch delay functionality with fixed/random options
- [x] Add per-request delays to avoid bot detection
- [x] Implement configuration persistence between sessions

## Pending Tasks

### Phase 2: Extract Utility Functions
- [x] Extract `RateLimiter` class to `core/rate_limiting.py`
- [x] Move task polling functions to `utils/task_polling.py`:
  - [x] `poll_task_result()`
  - [x] `is_task_id_response()`
- [x] Move URL processing functions to `utils/url_processing.py`:
  - [x] `get_processed_urls()`
- [x] Move title extraction functions to `parsers/title_extraction.py`:
  - [x] `extract_title_from_markdown()`
  - [x] `generate_safe_filename()`
- [x] Test functionality after each module is completed

### Phase 3: Extract Core Functionality
- [x] Move sitemap parsing functions to `parsers/sitemap_parser.py`:
  - [x] `parse_xml_file()`
  - [x] `get_urls_from_source()`
- [x] Move core crawler function to `core/crawler.py`:
  - [x] `crawl_parallel_with_rate_limiting()`
- [x] Test thoroughly after each module is completed

### Phase 4: Finalize Structure
- [x] Create a new `main.py` file with the refactored `main()` function
- [x] Update any remaining imports and references
- [x] Add proper docstrings and comments to all modules
- [x] Create a README.md for the package
- [x] Perform comprehensive testing of the entire application

## Testing Checklist
- [x] Verify all imports work correctly
- [x] Test crawling a small batch of URLs
- [x] Test error handling and reporting
- [x] Test task polling functionality
- [x] Test title extraction with different strategies
- [x] Verify memory usage monitoring works
- [x] Test rate limiting functionality
- [x] Test configuration persistence
- [x] Test per-request delays for bot detection avoidance

## Completed Enhancement: Markdown Cleaning

Implemented markdown cleaning functionality to improve the quality of crawled content:

### Phase 1: Design and Planning
- [x] Review existing clean_starlink_markdown.py script
- [x] Analyze raw and cleaned markdown samples
- [x] Determine implementation approach
- [x] Document tasks and implementation plan

### Phase 2: Core Implementation
- [x] Create new module `processors/markdown_cleaner.py`
  - [x] Extract metadata functions (title, URL, article ID, category)
  - [x] Implement content cleaning functions
  - [x] Add URL fixing and formatting functions
  - [x] Create YAML frontmatter generation

### Phase 3: Integration with Crawler
- [x] Add markdown cleaning options to `CrawlerConfig`
  - [x] Add `clean_markdown` boolean option
  - [x] Add cleaning-specific configuration options
- [x] Integrate cleaning step in crawler.py
  - [x] Add pre-save processing hook
  - [x] Implement file renaming with article IDs

### Phase 4: Standalone Processing
- [x] Create command-line entry point for post-processing
  - [x] Add batch processing capability
  - [x] Maintain compatibility with existing files
- [x] Update documentation
  - [x] Document new cleaning features in README.md
  - [x] Provide examples of both integrated and standalone use

### Phase 5: Testing and Refinement
- [x] Test integrated cleaning during crawling
- [x] Test standalone post-processing
- [x] Compare results with original clean_starlink_markdown.py
- [x] Optimize performance for large batches

### Phase 6: User Interface Implementation
- [x] Create `CleanerConfig` class in `config/cleaner_config.py`
  - [x] Add input/output directory options
  - [x] Add cleaning configuration options
  - [x] Set appropriate default values
- [x] Extend configuration persistence for cleaner
  - [x] Add save/load functions for cleaner config
  - [x] Store settings in ~/.starlink_cleaner_config.json
- [x] Implement interactive UI in `clean_markdown_ui.py`
  - [x] Display current settings
  - [x] Allow changing configuration options
  - [x] Preview files to be processed
  - [x] Show progress during processing
- [x] Create main entry point in `main_cleaner.py`
- [x] Fix title line break issues in YAML frontmatter
  - [x] Implement custom YAML frontmatter generation
  - [x] Ensure titles are properly quoted and displayed as a single line

## Future Enhancements
- [ ] Add proxy support for distributed crawling
- [ ] Implement user agent rotation
- [ ] Add support for authentication-protected sites
- [ ] Create a web interface for the crawler
- [ ] Implement advanced content extraction (tables, images)
