"""
Error handling utilities for the Starlink crawler.
This module provides error code extraction, categorization, and explanation.
"""

import re
import json
from typing import Dict, Tuple, Any

class ErrorInfo:
    """Class to handle error information and explanations"""
    
    # HTTP status code explanations
    HTTP_STATUS_CODES = {
        400: "Bad Request - The server cannot process the request due to a client error",
        401: "Unauthorized - Authentication is required and has failed or not been provided",
        403: "Forbidden - The server understood the request but refuses to authorize it",
        404: "Not Found - The requested resource could not be found",
        429: "Too Many Requests - Rate limiting has been applied",
        500: "Internal Server Error - The server has encountered a situation it doesn't know how to handle",
        502: "Bad Gateway - The server was acting as a gateway or proxy and received an invalid response",
        503: "Service Unavailable - The server is not ready to handle the request",
        504: "Gateway Timeout - The server is acting as a gateway and cannot get a response in time"
    }
    
    # Network error explanations
    NETWORK_ERRORS = {
        "ERR_CONNECTION_REFUSED": "Connection Refused - The target server refused the connection",
        "ERR_CONNECTION_RESET": "Connection Reset - The connection was reset during the operation",
        "ERR_CONNECTION_CLOSED": "Connection Closed - The connection was closed unexpectedly",
        "ERR_CONNECTION_TIMED_OUT": "Connection Timeout - The connection attempt timed out",
        "ERR_INTERNET_DISCONNECTED": "Internet Disconnected - No internet connection available",
        "ERR_NAME_NOT_RESOLVED": "DNS Error - The hostname could not be resolved",
        "ERR_ADDRESS_UNREACHABLE": "Address Unreachable - The IP address is unreachable",
        "ERR_FAILED": "General Failure - The operation failed for an unspecified reason",
        "ERR_HTTP_RESPONSE_CODE_FAILURE": "HTTP Response Code Failure - Received an error HTTP status code"
    }
    
    @staticmethod
    def get_error_code(error_msg):
        """Extract error code from error message
        
        Args:
            error_msg: The error message to parse
            
        Returns:
            str: The extracted error code or a generic error code
        """
        # Common error patterns
        patterns = [
            r'net::ERR_(\w+)',  # Chrome-style network errors
            r'NS_ERROR_(\w+)',   # Firefox-style network errors
            r'Error: (\d+)',     # HTTP status codes
            r'status=(\d+)',     # Another HTTP status format
            r'code="(\w+)"',    # XML/HTML error codes
            r'\[(\w+)\]',        # Bracketed error codes
            r'status code (\d+)' # Plain status code mention
        ]
        
        for pattern in patterns:
            match = re.search(pattern, error_msg)
            if match:
                return match.group(1)
        
        # If no specific code found, use a generic error code
        if 'timeout' in error_msg.lower():
            return 'TIMEOUT'
        elif 'memory' in error_msg.lower():
            return 'MEMORY_ISSUE'
        else:
            return 'UNKNOWN_ERROR'
    
    @staticmethod
    def extract_response_details(error_msg):
        """Extract HTTP status code and headers from error message if available
        
        Args:
            error_msg: The error message to parse
            
        Returns:
            Tuple[str, Dict]: The status code and headers extracted from the message
        """
        status_code = None
        headers = {}
        
        # Try to extract status code
        status_patterns = [
            r'status code (\d+)',
            r'status=(\d+)',
            r'Error: (\d+)'
        ]
        
        for pattern in status_patterns:
            match = re.search(pattern, error_msg)
            if match:
                status_code = match.group(1)
                break
        
        # Try to extract headers if they're in the error message
        headers_match = re.search(r'Headers:\s*({[^}]+})', error_msg)
        if headers_match:
            try:
                headers_str = headers_match.group(1)
                headers = json.loads(headers_str)
            except:
                pass
        
        return status_code, headers
    
    @staticmethod
    def get_explanation(error_code, error_msg):
        """Get explanation for error code
        
        Args:
            error_code: The error code to explain
            error_msg: The original error message for additional context
            
        Returns:
            str: A human-readable explanation of the error
        """
        # HTTP status code explanations
        http_status_explanations = {
            '400': "Bad Request - The server cannot process the request due to a client error",
            '401': "Unauthorized - Authentication is required and has failed or not been provided",
            '403': "Forbidden - The server understood the request but refuses to authorize it",
            '404': "Not Found - The requested resource could not be found",
            '429': "Too Many Requests - You have sent too many requests in a given amount of time",
            '500': "Internal Server Error - The server has encountered a situation it doesn't know how to handle",
            '502': "Bad Gateway - The server was acting as a gateway or proxy and received an invalid response",
            '503': "Service Unavailable - The server is not ready to handle the request",
            '504': "Gateway Timeout - The server was acting as a gateway or proxy and did not receive a timely response"
        }
        
        # Network error explanations
        network_error_explanations = {
            'ABORTED': "The operation was aborted",
            'CONNECTION_REFUSED': "Connection refused by the server",
            'CONNECTION_RESET': "Connection was reset",
            'CONNECTION_CLOSED': "Connection was closed",
            'CONNECTION_FAILED': "Connection failed",
            'NAME_NOT_RESOLVED': "DNS name resolution failed",
            'INTERNET_DISCONNECTED': "Internet connection is down",
            'ADDRESS_UNREACHABLE': "IP address is unreachable",
            'TIMEOUT': "The operation timed out",
            'FAILED': "The operation failed for unspecified reasons",
            'HTTP_RESPONSE_CODE_FAILURE': "HTTP Response Code Failure - Received an error HTTP status code",
            'MEMORY_ISSUE': "The operation failed due to memory constraints",
            'UNKNOWN_ERROR': "An unknown error occurred"
        }
        
        # Extract status code and headers from error message if available
        status_code, headers = ErrorInfo.extract_response_details(error_msg)
        
        # First check if we extracted a status code
        if status_code and status_code in http_status_explanations:
            return http_status_explanations[status_code]
        
        # Then check if the error code is an HTTP status code
        if error_code.isdigit() and error_code in http_status_explanations:
            return http_status_explanations[error_code]
        
        # Then check if it's a known network error
        if error_code in network_error_explanations:
            return network_error_explanations[error_code]
        
        # For unknown codes, provide a generic explanation
        return f"Error code {error_code} - No detailed explanation available"

    @staticmethod
    def get_error_explanation(error_message: str) -> Tuple[str, str]:
        """Extract error code and provide explanation from an error message
        
        Args:
            error_message: The error message to parse and explain
            
        Returns:
            Tuple[str, str]: A tuple containing (error_code, explanation)
        """
        # Check for HTTP status code
        http_match = re.search(r'status=([0-9]{3})', error_message)
        if http_match:
            status_code = int(http_match.group(1))
            explanation = ErrorInfo.HTTP_STATUS_CODES.get(
                status_code, 
                f"HTTP {status_code} - Unknown HTTP status code"
            )
            return f"HTTP {status_code}", explanation
        
        # Check for network errors
        for error_code, explanation in ErrorInfo.NETWORK_ERRORS.items():
            if error_code in error_message:
                return error_code, explanation
        
        # If no specific error found
        return "UNKNOWN_ERROR", "Unknown error - Could not determine the specific error type"