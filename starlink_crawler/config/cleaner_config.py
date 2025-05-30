"""
Configuration class for the Starlink markdown cleaner.
This module defines the configuration settings for the markdown cleaner.
"""

import os
from typing import Optional

class CleanerConfig:
    """Configuration class for markdown cleaner settings"""
    def __init__(
        self,
        input_dir: str = "starlink_markdown_output_files",
        output_dir: str = "starlink_markdown_output_files_clean",
        extract_metadata: bool = True,
        fix_urls: bool = True,
        remove_navigation: bool = True,
        remove_footer: bool = True,
        add_frontmatter: bool = True,
        language: str = "en",
        batch_mode: bool = False,
        pattern: Optional[str] = None,
        limit: Optional[int] = None
    ):
        """Initialize cleaner configuration with default values.
        
        Args:
            input_dir: Directory containing markdown files to process
            output_dir: Directory to save processed files
            extract_metadata: Whether to extract metadata from content
            fix_urls: Whether to fix malformed URLs
            remove_navigation: Whether to remove navigation elements
            remove_footer: Whether to remove footer content
            add_frontmatter: Whether to add YAML frontmatter
            language: Content language (default: en)
            batch_mode: Whether to process all files without confirmation
            pattern: Optional glob pattern to filter files (e.g., "*.md")
            limit: Optional limit on number of files to process
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.extract_metadata = extract_metadata
        self.fix_urls = fix_urls
        self.remove_navigation = remove_navigation
        self.remove_footer = remove_footer
        self.add_frontmatter = add_frontmatter
        self.language = language
        self.batch_mode = batch_mode
        self.pattern = pattern
        self.limit = limit
        
        # Create output directory if specified
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
