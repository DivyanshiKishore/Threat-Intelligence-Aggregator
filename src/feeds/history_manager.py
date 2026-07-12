"""
Feed execution history manager.
"""

from datetime import datetime

from .history import FeedExecutionHistory
from .result import FeedExecutionResult


class FeedHistoryManager:
    """
    Stores execution history for feeds.
    """

    def __init__(self) -> None:
        self._history: dict[str, FeedExecutionHistory] = {}

    def update(
        self,
        result: FeedExecutionResult,
    ) -> None:
        """
        Update execution history using a scheduler result.
        """

        history = self._history.setdefault(
            result.feed_name,
            FeedExecutionHistory(feed_name=result.feed_name),
        )

        now = datetime.now()

        history.last_run = now
        history.total_runs += 1
        history.total_iocs += result.ioc_count

        if result.success:
            history.successful_runs += 1
            history.last_success = now
        else:
            history.failed_runs += 1
            history.last_failure = now

    def get(
        self,
        feed_name: str,
    ) -> FeedExecutionHistory | None:
        return self._history.get(feed_name)

    def get_all(self) -> list[FeedExecutionHistory]:
        return list(self._history.values())