"""
Sitemap parsing utilities for the Starlink crawler.
This module provides functions to extract URLs from XML sitemaps.
"""

import os
import requests
from typing import List
from xml.etree import ElementTree

async def parse_xml_file(file_path) -> List[str]:
    """
    Parse a local XML sitemap file to extract URLs.
    
    Args:
        file_path: Path to the XML file
        
    Returns:
        List[str]: List of URLs extracted from the XML file
    """
    print(f"\nParsing XML file: {file_path}")
    
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"Error: XML file not found at {file_path}")
            return []
            
        # Read and parse the XML file
        with open(file_path, 'r', encoding='utf-8') as f:
            xml_content = f.read()
            
        # Parse the XML
        root = ElementTree.fromstring(xml_content)
        
        # Extract all URLs from the sitemap
        # The namespace is usually defined in the root element
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]
        
        return urls
        
    except Exception as e:
        print(f"Error parsing XML file: {e}")
        return []

async def get_urls_from_source(source_type, source_path) -> List[str]:
    """
    Get URLs from either a sitemap URL or a local XML file.
    
    Args:
        source_type: Type of source ('url' or 'file')
        source_path: URL or file path to the sitemap
        
    Returns:
        List[str]: List of URLs
    """
    if source_type == 'url':
        # URL of the sitemap
        print(f"\nFetching URLs from: {source_path}")
        
        # Try to fetch and parse the sitemap
        try:
            response = requests.get(source_path)
            response.raise_for_status()
            
            # Parse the XML
            root = ElementTree.fromstring(response.content)
            
            # Extract all URLs from the sitemap
            # The namespace is usually defined in the root element
            namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]
            
            return urls
            
        except Exception as e:
            print(f"Error fetching sitemap: {e}")
            return []
    elif source_type == 'file':
        return await parse_xml_file(source_path)
    else:
        print(f"Unsupported source type: {source_type}")
        return []