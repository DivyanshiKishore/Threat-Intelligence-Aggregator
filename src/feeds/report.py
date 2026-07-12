"""
Feed execution reporting.
"""

from dataclasses import dataclass

from .result import FeedExecutionResult


@dataclass(slots=True)
class FeedExecutionReport:
    total_feeds: int
    successful_feeds: int
    failed_feeds: int
    total_iocs: int
    total_execution_time: float


class FeedReportGenerator:
    """
    Generates execution summary from scheduler results.
    """

    @staticmethod
    def generate(
        results: list[FeedExecutionResult],
    ) -> FeedExecutionReport:

        return FeedExecutionReport(
            total_feeds=len(results),
            successful_feeds=sum(
                1 for r in results if r.success
            ),
            failed_feeds=sum(
                1 for r in results if not r.success
            ),
            total_iocs=sum(
                r.ioc_count for r in results
            ),
            total_execution_time=sum(
                r.execution_time for r in results
            ),
        )