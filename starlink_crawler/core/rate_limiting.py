"""
Rate limiting functionality for the Starlink crawler.
This module provides a token bucket rate limiter for controlling request rates.
"""

import time
import asyncio

class RateLimiter:
    """Simple token bucket rate limiter"""
    def __init__(self, rate: float, burst: int = 1):
        """Initialize a token bucket rate limiter.
        
        Args:
            rate: Tokens per second (e.g., 0.2 for 1 request per 5 seconds)
            burst: Maximum number of tokens that can be accumulated
        """
        self.rate = rate  # tokens per second
        self.burst = burst  # max tokens
        self.tokens = burst  # current tokens
        self.last_time = time.time()
    
    async def acquire(self):
        """Acquire a token, waiting if necessary.
        
        This is an async method that will block until a token is available.
        It implements the token bucket algorithm, where tokens are added
        at a constant rate up to the burst limit.
        """
        while True:
            # Update tokens based on elapsed time
            now = time.time()
            elapsed = now - self.last_time
            self.tokens = min(self.burst, self.tokens + elapsed * self.rate)
            self.last_time = now
            
            if self.tokens >= 1:
                break
            else:
                # Wait a bit before checking again
                await asyncio.sleep(0.1)
        self.tokens -= 1