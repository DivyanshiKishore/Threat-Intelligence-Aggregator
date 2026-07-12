from src.feeds.history_manager import FeedHistoryManager
from src.feeds.result import FeedExecutionResult


def test_update_success():
    manager = FeedHistoryManager()

    result = FeedExecutionResult(
        feed_name="test_feed",
        success=True,
        ioc_count=10,
        execution_time=1.2,
    )

    manager.update(result)

    history = manager.get("test_feed")

    assert history is not None
    assert history.feed_name == "test_feed"
    assert history.total_runs == 1
    assert history.successful_runs == 1
    assert history.failed_runs == 0
    assert history.total_iocs == 10
    assert history.last_run is not None
    assert history.last_success is not None


def test_update_failure():
    manager = FeedHistoryManager()

    result = FeedExecutionResult(
        feed_name="test_feed",
        success=False,
        ioc_count=0,
        execution_time=0.8,
        error="Download failed",
    )

    manager.update(result)

    history = manager.get("test_feed")

    assert history is not None
    assert history.total_runs == 1
    assert history.successful_runs == 0
    assert history.failed_runs == 1
    assert history.last_failure is not None


def test_multiple_updates():
    manager = FeedHistoryManager()

    manager.update(
        FeedExecutionResult(
            feed_name="test_feed",
            success=True,
            ioc_count=5,
            execution_time=0.5,
        )
    )

    manager.update(
        FeedExecutionResult(
            feed_name="test_feed",
            success=False,
            ioc_count=0,
            execution_time=0.4,
            error="Error",
        )
    )

    history = manager.get("test_feed")

    assert history is not None
    assert history.total_runs == 2
    assert history.successful_runs == 1
    assert history.failed_runs == 1
    assert history.total_iocs == 5


def test_get_all():
    manager = FeedHistoryManager()

    manager.update(
        FeedExecutionResult(
            feed_name="feed1",
            success=True,
            ioc_count=1,
            execution_time=0.1,
        )
    )

    manager.update(
        FeedExecutionResult(
            feed_name="feed2",
            success=True,
            ioc_count=2,
            execution_time=0.2,
        )
    )

    histories = manager.get_all()

    assert len(histories) == 2