#!/usr/bin/env python3
"""
Interactive UI for the Starlink Markdown Cleaner.

This module provides a user-friendly interface for configuring and running
the markdown cleaner. It allows users to:
- Configure cleaning options
- Save and load configurations
- Process markdown files with a simple interface
"""

import os
import sys
import glob
import argparse
from typing import List, Optional

# Add the parent directory to the path to allow importing the package when run directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import from our package - handle both package import and direct script execution
try:
    # When imported as a package
    from starlink_crawler.config.cleaner_config import CleanerConfig
    from starlink_crawler.config.config_persistence import (
        load_cleaner_config, save_cleaner_config, create_cleaner_config_from_dict
    )
    from starlink_crawler.processors.markdown_cleaner import MarkdownCleaner
except ImportError:
    # When run directly from the starlink_crawler directory
    from config.cleaner_config import CleanerConfig
    from config.config_persistence import (
        load_cleaner_config, save_cleaner_config, create_cleaner_config_from_dict
    )
    from processors.markdown_cleaner import MarkdownCleaner


def prompt_for_settings(config: CleanerConfig) -> CleanerConfig:
    """
    Prompt the user for cleaner settings.
    
    Args:
        config: Current CleanerConfig instance
        
    Returns:
        Updated CleanerConfig instance
    """
    print("\n=== Cleaner Settings ===")
    
    # Input directory
    input_dir = input(f"Input directory [{config.input_dir}]: ")
    if input_dir.strip():
        config.input_dir = input_dir.strip()
    
    # Output directory
    output_dir = input(f"Output directory [{config.output_dir}]: ")
    if output_dir.strip():
        config.output_dir = output_dir.strip()
    
    # Extract metadata
    extract_metadata = input(f"Extract metadata (y/n) [{('y' if config.extract_metadata else 'n')}]: ")
    if extract_metadata.strip().lower() in ('y', 'n'):
        config.extract_metadata = extract_metadata.strip().lower() == 'y'
    
    # Fix URLs
    fix_urls = input(f"Fix malformed URLs (y/n) [{('y' if config.fix_urls else 'n')}]: ")
    if fix_urls.strip().lower() in ('y', 'n'):
        config.fix_urls = fix_urls.strip().lower() == 'y'
    
    # Remove navigation
    remove_navigation = input(f"Remove navigation elements (y/n) [{('y' if config.remove_navigation else 'n')}]: ")
    if remove_navigation.strip().lower() in ('y', 'n'):
        config.remove_navigation = remove_navigation.strip().lower() == 'y'
    
    # Remove footer
    remove_footer = input(f"Remove footer content (y/n) [{('y' if config.remove_footer else 'n')}]: ")
    if remove_footer.strip().lower() in ('y', 'n'):
        config.remove_footer = remove_footer.strip().lower() == 'y'
    
    # Add frontmatter
    add_frontmatter = input(f"Add YAML frontmatter (y/n) [{('y' if config.add_frontmatter else 'n')}]: ")
    if add_frontmatter.strip().lower() in ('y', 'n'):
        config.add_frontmatter = add_frontmatter.strip().lower() == 'y'
    
    # Language
    language = input(f"Content language [{config.language}]: ")
    if language.strip():
        config.language = language.strip()
    
    # Batch mode
    batch_mode = input(f"Process all files without confirmation (y/n) [{('y' if config.batch_mode else 'n')}]: ")
    if batch_mode.strip().lower() in ('y', 'n'):
        config.batch_mode = batch_mode.strip().lower() == 'y'
    
    # File pattern
    pattern = input(f"File pattern (e.g., *.md) [{'*' if not config.pattern else config.pattern}]: ")
    if pattern.strip():
        config.pattern = pattern.strip()
    elif pattern.strip() == '*':
        config.pattern = None
    
    # File limit
    limit_str = input(f"Limit number of files (0 for no limit) [{config.limit if config.limit else 0}]: ")
    if limit_str.strip() and limit_str.strip().isdigit():
        limit = int(limit_str.strip())
        config.limit = limit if limit > 0 else None
    
    return config


def get_markdown_files(input_dir: str, pattern: Optional[str] = None, limit: Optional[int] = None) -> List[str]:
    """
    Get a list of markdown files from the input directory.
    
    Args:
        input_dir: Directory to search for markdown files
        pattern: Optional glob pattern to filter files
        limit: Optional limit on number of files to return
        
    Returns:
        List of file paths
    """
    if not os.path.isdir(input_dir):
        print(f"Error: Input directory '{input_dir}' not found")
        return []
    
    # Use pattern if provided, otherwise default to *.md
    search_pattern = pattern if pattern else "*.md"
    file_paths = glob.glob(os.path.join(input_dir, search_pattern))
    
    # Filter to only include files (not directories)
    file_paths = [path for path in file_paths if os.path.isfile(path)]
    
    # Sort files for consistent ordering
    file_paths.sort()
    
    # Apply limit if specified
    if limit and len(file_paths) > limit:
        file_paths = file_paths[:limit]
    
    return file_paths


def process_files(config: CleanerConfig) -> bool:
    """
    Process markdown files based on the configuration.
    
    Args:
        config: CleanerConfig instance
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Create output directory if it doesn't exist
    os.makedirs(config.output_dir, exist_ok=True)
    
    # Get list of markdown files
    files = get_markdown_files(config.input_dir, config.pattern, config.limit)
    if not files:
        print(f"No markdown files found in '{config.input_dir}'")
        return False
    
    # Show files to be processed
    print(f"\nFound {len(files)} markdown files to process:")
    for i, file_path in enumerate(files[:5], 1):
        print(f"  {i}. {os.path.basename(file_path)}")
    if len(files) > 5:
        print(f"  ... and {len(files) - 5} more files")
    
    # Ask for confirmation if not in batch mode
    if not config.batch_mode:
        confirm = input("\nDo you want to process these files? (y/n): ")
        if confirm.lower() != 'y':
            print("Operation cancelled by user.")
            return False
    
    # Initialize cleaner with configuration
    cleaner = MarkdownCleaner(
        extract_metadata=config.extract_metadata,
        fix_urls=config.fix_urls,
        remove_navigation=config.remove_navigation,
        remove_footer=config.remove_footer,
        add_frontmatter=config.add_frontmatter,
        language=config.language
    )
    
    # Process each file
    print("\nProcessing files...")
    for i, file_path in enumerate(files, 1):
        filename = os.path.basename(file_path)
        print(f"[{i}/{len(files)}] Processing {filename}...")
        try:
            output_path, article_id = cleaner.process_file(file_path, config.output_dir)
            print(f"  Saved to: {os.path.basename(output_path)}")
        except Exception as e:
            print(f"  Error processing {filename}: {e}")
    
    print(f"\nProcessing complete! {len(files)} files processed.")
    print(f"Cleaned files saved to: {config.output_dir}/")
    return True


def run_cleaner_ui():
    """Run the interactive UI for the markdown cleaner."""
    print("\n=== Starlink Markdown Cleaner ===\n")
    
    # Try to load saved configuration
    config_dict = load_cleaner_config()
    if config_dict:
        config = create_cleaner_config_from_dict(config_dict)
        print("Loaded saved configuration.")
    else:
        config = CleanerConfig()
        print("Using default configuration.")
    
    # Display current settings
    print("\nCurrent settings:")
    print(f"  Input directory: {config.input_dir}")
    print(f"  Output directory: {config.output_dir}")
    print(f"  Extract metadata: {config.extract_metadata}")
    print(f"  Fix URLs: {config.fix_urls}")
    print(f"  Remove navigation: {config.remove_navigation}")
    print(f"  Remove footer: {config.remove_footer}")
    print(f"  Add frontmatter: {config.add_frontmatter}")
    print(f"  Language: {config.language}")
    print(f"  Batch mode: {config.batch_mode}")
    print(f"  File pattern: {config.pattern if config.pattern else '*'}")
    print(f"  File limit: {config.limit if config.limit else 'No limit'}")
    
    # Allow user to change settings
    change_settings = input("\nDo you want to change these settings? (y/n): ")
    if change_settings.lower() == 'y':
        config = prompt_for_settings(config)
    
    # Ask to save configuration
    save_settings = input("\nSave these settings for future use? (y/n): ")
    if save_settings.lower() == 'y':
        if save_cleaner_config(config):
            print("Settings saved successfully.")
        else:
            print("Failed to save settings.")
    
    # Confirm and run
    confirm = input("\nStart cleaning markdown files? (y/n): ")
    if confirm.lower() == 'y':
        process_files(config)
    else:
        print("Operation cancelled by user.")


def main():
    """Main entry point for the cleaner UI."""
    parser = argparse.ArgumentParser(
        description='Starlink Markdown Cleaner UI',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--input-dir', help='Input directory containing markdown files')
    parser.add_argument('--output-dir', help='Output directory for processed files')
    parser.add_argument('--batch', action='store_true', help='Run in batch mode without interactive prompts')
    
    args = parser.parse_args()
    
    if args.batch and (args.input_dir or args.output_dir):
        # Run in batch mode with command-line arguments
        config_dict = load_cleaner_config()
        if config_dict:
            config = create_cleaner_config_from_dict(
                config_dict,
                input_dir=args.input_dir,
                output_dir=args.output_dir
            )
        else:
            config = CleanerConfig(
                input_dir=args.input_dir or "starlink_markdown_output_files",
                output_dir=args.output_dir or "starlink_markdown_output_files_clean",
                batch_mode=True
            )
        
        process_files(config)
    else:
        # Run interactive UI
        run_cleaner_ui()


if __name__ == "__main__":
    main()
