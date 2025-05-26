# Starlink Crawler Modularization Plan

## Project Overview
The goal of this project is to modularize the `crawl_starlink_parallel.py` script (approximately 1,200 lines) into a more maintainable package structure with smaller, focused modules.

## Modularization Approach

### Phase 1: Set Up Package Structure and Extract Core Classes ✅
**Goal**: Create the basic package structure and move the most independent classes first.

1. Create the basic directory structure with `__init__.py` files ✅
2. Extract the `TitleStrategy` and `CrawlerConfig` classes to their own modules ✅
3. Extract the `ErrorInfo` and `CrawlStats` classes ✅
4. Update imports in the main file ✅
5. Test to ensure everything still works

### Phase 2: Extract Utility Functions
**Goal**: Move utility functions to their appropriate modules.

1. Extract `RateLimiter` class to its own module
2. Move task polling functions (`poll_task_result`, `is_task_id_response`)
3. Move URL processing functions (`get_processed_urls`)
4. Move title extraction functions (`extract_title_from_markdown`, `generate_safe_filename`)
5. Test functionality after each move

### Phase 3: Extract Sitemap Parsing and Core Crawler Logic
**Goal**: Move the more complex, core functionality.

1. Extract sitemap parsing functions (`parse_xml_file`, `get_urls_from_source`)
2. Move the core crawler function (`crawl_parallel_with_rate_limiting`)
3. Test thoroughly after each move

### Phase 4: Refactor Main Function and Finalize Structure
**Goal**: Clean up the main file and finalize the package structure.

1. Refactor the `main()` function to use all the modularized components
2. Update any remaining imports and references
3. Add proper docstrings and comments to clarify module purposes
4. Create a simple README for the package
5. Comprehensive testing of the entire application

## Directory Structure
```
starlink_crawler/
│
├── __init__.py                  # Makes the directory a package
│
├── main.py                      # Entry point (renamed from crawl_starlink_parallel.py)
│
├── config/
│   ├── __init__.py
│   ├── crawler_config.py        # CrawlerConfig class
│   └── title_strategy.py        # TitleStrategy class
│
├── core/
│   ├── __init__.py
│   ├── crawler.py               # Main crawling logic
│   └── rate_limiting.py         # RateLimiter class
│
├── utils/
│   ├── __init__.py
│   ├── error_handling.py        # ErrorInfo class
│   ├── stats.py                 # CrawlStats class
│   ├── task_polling.py          # Task polling functions
│   └── url_processing.py        # URL processing utilities
│
├── parsers/
│   ├── __init__.py
│   ├── sitemap_parser.py        # XML parsing functions
│   └── title_extraction.py      # Title extraction functions
│
└── data/                        # Optional directory for output data
    └── __init__.py
```

## Implementation Considerations
- Each module should have clear docstrings explaining its purpose
- Modules should have minimal dependencies on each other
- The `CrawlerConfig` class will be used to share configuration across modules
- All modules will be organized under the common `starlink_crawler` package
