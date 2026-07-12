from src.feeds.report import FeedReportGenerator
from src.feeds.result import FeedExecutionResult


def test_generate_report():
    results = [
        FeedExecutionResult(
            feed_name="feed1",
            success=True,
            ioc_count=10,
            execution_time=1.5,
        ),
        FeedExecutionResult(
            feed_name="feed2",
            success=False,
            ioc_count=0,
            execution_time=0.5,
            error="Download failed",
        ),
    ]

    report = FeedReportGenerator.generate(results)

    assert report.total_feeds == 2
    assert report.successful_feeds == 1
    assert report.failed_feeds == 1
    assert report.total_iocs == 10
    assert report.total_execution_time == 2.0