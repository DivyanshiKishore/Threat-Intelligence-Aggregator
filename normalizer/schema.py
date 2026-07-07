"""

IOC schema used throughout the Threat Intelligence Aggregator.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class IOC:
    """
    Standard representation of an Indicator of Compromise (IOC).
    """

    type: str
    value: str
    source: str

    confidence: int = 0

    tags: List[str] = field(default_factory=list)

    first_seen: Optional[str] = None
    last_seen: Optional[str] = None