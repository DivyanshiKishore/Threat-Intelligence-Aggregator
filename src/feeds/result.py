"""
Feed execution result model.
"""

from dataclasses import dataclass, field
from typing import Optional

from normalizer.schema import IOC



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
    iocs: list[IOC] = field(default_factory=list)