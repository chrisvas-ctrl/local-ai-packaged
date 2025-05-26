"""
Title extraction strategy definitions for the Starlink crawler.
This module defines different strategies for extracting titles from web pages.
"""

class TitleStrategy:
    """Enum-like class for title extraction strategies"""
    HEADING_FIRST = "heading_first"  # Try headings first, then first line, then URL
    URL_FIRST = "url_first"          # Try URL path first, then headings, then first line
    FIRST_LINE_FIRST = "first_line_first"  # Try first line first, then headings, then URL
    HEADING_ONLY = "heading_only"    # Only use headings, fall back to URL + timestamp
    URL_ONLY = "url_only"            # Only use URL path, fall back to domain + timestamp
    
    @staticmethod
    def get_description(strategy):
        """Return a human-readable description of the title strategy.
        
        Args:
            strategy: The strategy identifier
            
        Returns:
            str: Description of the strategy
        """
        descriptions = {
            TitleStrategy.HEADING_FIRST: "Extract from headings first, then first line, then URL",
            TitleStrategy.URL_FIRST: "Extract from URL path first, then headings, then first line",
            TitleStrategy.FIRST_LINE_FIRST: "Extract from first line first, then headings, then URL",
            TitleStrategy.HEADING_ONLY: "Only extract from headings (# or ## or ###)",
            TitleStrategy.URL_ONLY: "Only extract from URL path"
        }
        return descriptions.get(strategy, "Unknown strategy")