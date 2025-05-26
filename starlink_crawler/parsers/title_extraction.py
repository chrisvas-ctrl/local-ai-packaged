"""
Title extraction utilities for the Starlink crawler.
This module provides functions to extract and generate titles from markdown content and URLs.
"""

import re
import hashlib
from datetime import datetime
from urllib.parse import urlparse

# Import from our package
from starlink_crawler.config import TitleStrategy

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