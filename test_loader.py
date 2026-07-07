from pathlib import Path
from feeds.loader import FeedLoader

loader = FeedLoader(Path("feeds"))

feeds = loader.discover()

for feed in feeds:
    print(feed)