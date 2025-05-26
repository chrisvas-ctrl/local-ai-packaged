"""
Statistics tracking for the Starlink crawler.
This module provides functionality to track and report crawling statistics.
"""

import os
import json
import psutil
from datetime import datetime
from typing import Dict, Tuple, Optional

class CrawlStats:
    """Tracks crawling statistics"""
    def __init__(self):
        """Initialize statistics tracking"""
        self.success_count = 0
        self.fail_count = 0
        self.skipped_count = 0  # Count of skipped URLs
        self.peak_memory = 0
        self.start_time = datetime.now()
        self.process = psutil.Process(os.getpid())
        self.errors = {}  # Dictionary to track errors by URL
        self.skipped = {}  # Dictionary to track skipped URLs
        # Track crawl timestamps for rate limiting
        self.crawl_timestamps = []

    def log_memory(self, prefix: str = "") -> None:
        """Log current and peak memory usage
        
        Args:
            prefix: Optional prefix for the log message
        """
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