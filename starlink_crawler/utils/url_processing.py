"""
URL processing utilities for the Starlink crawler.
This module provides functions to track and manage processed URLs.
"""

import os
import re
import glob
from typing import Set, Tuple

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