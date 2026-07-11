import json
import pytest

from src.feeds.loaders.json_loader import JSONFeedLoader
from src.feeds.loaders.yaml_loader import YAMLFeedLoader


@pytest.fixture
def feed_data():

    return {
        "feeds": [
            {
                "name": "test_feed",
                "url": "https://example.com/feed.txt",
                "parser_type": "txt",
                "enabled": True,
                "update_interval": 3600,
                "tags": [
                    "malware"
                ]
            }
        ]
    }


def test_json_loader(tmp_path, feed_data):

    file = tmp_path / "feeds.json"

    file.write_text(
        json.dumps(feed_data)
    )

    loader = JSONFeedLoader()

    registry = loader.load(str(file))

    assert registry.count() == 1

    assert (
        registry.get("test_feed").name
        ==
        "test_feed"
    )


def test_yaml_loader(tmp_path):

    file = tmp_path / "feeds.yaml"

    file.write_text(
        """
feeds:
  - name: test_feed
    url: https://example.com/feed.txt
    parser_type: txt
    enabled: true
    update_interval: 3600
    tags:
      - malware
"""
    )

    loader = YAMLFeedLoader()

    registry = loader.load(str(file))

    assert registry.count() == 1

    assert (
        registry.get("test_feed").parser_type
        ==
        "txt"
    )