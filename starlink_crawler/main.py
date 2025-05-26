"""
Main entry point for the Starlink crawler.
This module provides the command-line interface and user interaction for the crawler.
"""

import os
import asyncio

# Import from our package
from starlink_crawler.config import TitleStrategy, CrawlerConfig
from starlink_crawler.parsers import get_urls_from_source
from starlink_crawler.core import crawl_parallel_with_rate_limiting

# Set up directory structure for output files
__location__ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Parent directory
__output__ = os.path.join(__location__, "starlink_markdown_output_files")    # Directory for markdown output files
os.makedirs(__output__, exist_ok=True)

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
        
        # Create a default config instance with our preferred title strategy
        # This ensures we use the defaults from CrawlerConfig for everything else
        default_config_obj = CrawlerConfig(
            output_dir=__output__,
            title_strategy=TitleStrategy.URL_FIRST  # Override default title strategy
        )
        
        # Extract values from the config object for UI display and customization
        default_config = {
            "batch_size": None,  # Not part of CrawlerConfig
            "max_concurrent": default_config_obj.max_concurrent,
            "request_rate": default_config_obj.request_rate,
            "dynamic_delay": default_config_obj.dynamic_delay,
            "min_delay": default_config_obj.min_batch_delay,
            "max_delay": default_config_obj.max_batch_delay,
            "max_crawls_per_minute": default_config_obj.max_crawls_per_minute,
            "title_strategy": default_config_obj.title_strategy,
            "skip_existing": default_config_obj.skip_existing,
            "task_poll_interval": default_config_obj.task_poll_interval,
            "max_task_polls": default_config_obj.max_task_polls
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
        print(f"Delay range: {default_config['min_delay']}-{default_config['max_delay']} seconds (randomized)")
        print(f"Max crawls per minute: {default_config['max_crawls_per_minute']}")
        print(f"Title strategy: {TitleStrategy.get_description(default_config['title_strategy'])}")
        print(f"Skip existing: {'Yes (only successful files)' if default_config['skip_existing'] else 'No'}")
        print(f"Task polling: {default_config['max_task_polls']} attempts every {default_config['task_poll_interval']} seconds")
        
        # Ask if user wants to use defaults or customize
        customize = input("\nUse these default settings? (y/n, default: y): ").lower() == 'n'
        
        # Initialize with defaults
        batch_size = default_config['batch_size']
        max_concurrent = default_config['max_concurrent']
        request_rate = default_config['request_rate']
        dynamic_delay = default_config['dynamic_delay']
        min_delay = default_config['min_delay']
        max_delay = default_config['max_delay']
        max_crawls_per_minute = default_config['max_crawls_per_minute']
        title_strategy = default_config['title_strategy']
        skip_existing = default_config['skip_existing']
        task_poll_interval = default_config['task_poll_interval']
        max_task_polls = default_config['max_task_polls']
        
        # If customization is requested, ask for each parameter
        if customize:
            # Ask for batch size
            try:
                batch_input = input("\nBatch size (empty for all URLs): ")
                if batch_input:
                    batch_size = int(batch_input)
                    if batch_size <= 0 or batch_size > total_urls:
                        print(f"Invalid batch size, using all {total_urls} URLs")
                        batch_size = None
            except ValueError:
                print("Invalid input, using all URLs")
                batch_size = None
                
            # Ask for max concurrent
            try:
                concurrent_input = input(f"\nMax concurrent crawlers (default: {max_concurrent}): ")
                if concurrent_input:
                    max_concurrent = int(concurrent_input)
                    if max_concurrent <= 0:
                        print("Invalid value, using default")
                        max_concurrent = default_config['max_concurrent']
            except ValueError:
                print("Invalid input, using default value")
                
            # Ask for request rate
            try:
                rate_input = input(f"\nRequest rate per second (default: {request_rate}): ")
                if rate_input:
                    request_rate = float(rate_input)
                    if request_rate <= 0:
                        print("Invalid value, using default")
                        request_rate = default_config['request_rate']
            except ValueError:
                print("Invalid input, using default value")
                
            # Ask for dynamic delay
            dynamic_input = input(f"\nUse dynamic delay based on error rates? (y/n, default: {'y' if dynamic_delay else 'n'}): ").lower()
            if dynamic_input in ['y', 'n']:
                dynamic_delay = (dynamic_input == 'y')
                
            # Ask for min delay
            try:
                min_delay_input = input(f"\nMinimum delay between batches in seconds (default: {min_delay}): ")
                if min_delay_input:
                    min_delay = float(min_delay_input)
                    if min_delay < 0:
                        print("Invalid value, using default")
                        min_delay = default_config['min_delay']
            except ValueError:
                print("Invalid input, using default value")
                
            # Ask for max delay
            try:
                max_delay_input = input(f"\nMaximum delay between batches in seconds (default: {max_delay}): ")
                if max_delay_input:
                    max_delay = float(max_delay_input)
                    if max_delay < min_delay:
                        print(f"Max delay must be >= min delay ({min_delay}), using default")
                        max_delay = default_config['max_delay']
            except ValueError:
                print("Invalid input, using default value")
                
            # Ask for max crawls per minute
            try:
                max_crawls_input = input(f"\nMax crawls per minute (0 for no limit, default: {max_crawls_per_minute}): ")
                if max_crawls_input:
                    max_crawls_per_minute = int(max_crawls_input)
            except ValueError:
                print("Invalid input, using default value")
                
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
                
            # Ask for task polling interval
            try:
                poll_interval_input = input(f"\nTask polling interval in seconds (default: {task_poll_interval}): ")
                if poll_interval_input:
                    task_poll_interval = float(poll_interval_input)
            except ValueError:
                print("Invalid input, using default value")
                
            # Ask for maximum task polling attempts
            try:
                max_polls_input = input(f"\nMaximum task polling attempts (default: {max_task_polls}): ")
                if max_polls_input:
                    max_task_polls = int(max_polls_input)
            except ValueError:
                print("Invalid input, using default value")
            
        # Create crawler configuration
        config = CrawlerConfig(
            max_concurrent=max_concurrent,
            memory_threshold=70.0,
            min_batch_delay=min_delay,
            max_batch_delay=max_delay,
            dynamic_delay=dynamic_delay,
            request_rate=request_rate,
            burst=2,
            max_crawls_per_minute=max_crawls_per_minute,
            output_dir=__output__,
            title_strategy=title_strategy,
            skip_existing=skip_existing,
            task_poll_interval=task_poll_interval,
            max_task_polls=max_task_polls
        )
        
        # Calculate and show processing time (approximate)
        process_urls = batch_size if batch_size else total_urls
        # Estimate time based on number of batches and rate limiting
        num_batches = (process_urls + config.max_concurrent - 1) // config.max_concurrent
        # Use average of min and max delay for estimation
        avg_batch_delay = (config.min_batch_delay + config.max_batch_delay) / 2
        process_time = (num_batches * (1/config.request_rate + avg_batch_delay)) / 60
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

def run():
    """Entry point for the command-line interface."""
    asyncio.run(main())

if __name__ == "__main__":
    run()