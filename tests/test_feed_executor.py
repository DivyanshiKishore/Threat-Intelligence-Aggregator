from unittest.mock import MagicMock

from src.feeds.executor import FeedExecutor
from src.feeds.registry import FeedRegistry
from src.feeds.result import FeedExecutionResult


def test_executor_executes_scheduler(monkeypatch):
    loader = MagicMock()
    registry = FeedRegistry()

    loader.load.return_value = registry

    downloader = MagicMock()
    pipeline = MagicMock()

    expected_results = [
        FeedExecutionResult(
            feed_name="test_feed",
            success=True,
            ioc_count=5,
            execution_time=0.10,
        )
    ]

    class DummyScheduler:
        def __init__(
            self,
            registry,
            downloader,
            pipeline_processor,
            history_manager=None,
        ):

            self.registry = registry
            self.downloader = downloader
            self.piple_processor = pipeline_processor
            self.history_manager= history_manager

            
        def run(self):
            return expected_results

    monkeypatch.setattr(
        "src.feeds.executor.FeedScheduler",
        DummyScheduler,
    )

    executor = FeedExecutor(
        loader,
        downloader,
        pipeline,
    )

    results = executor.execute("feeds.yaml")

    loader.load.assert_called_once_with("feeds.yaml")

    assert results == expected_results
    assert len(results) == 1
    assert results[0].success is True