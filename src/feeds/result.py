"""
Feed execution result model.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class FeedExecutionResult:
    """
    Stores feed processing outcome.
    """

    feed_name: str
    success: bool
    ioc_count: int = 0
    execution_time: float = 0.0
    error: Optional[str] = None