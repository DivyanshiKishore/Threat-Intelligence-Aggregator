"""
Feed execution history models.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class FeedExecutionHistory:
    """
    Stores the latest execution information for a feed.
    """

    feed_name: str
    last_run: datetime | None = None
    last_success: datetime | None = None
    last_failure: datetime | None = None
    total_runs: int = 0
    successful_runs: int = 0
    failed_runs: int = 0
    total_iocs: int = 0