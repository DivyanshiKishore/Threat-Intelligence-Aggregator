from config import FeedConfig
from downloader.feed_downloader import FeedDownloader
from utils.logger import get_logger

logger = get_logger("Main")

downloader = FeedDownloader()

if not FeedConfig.JSON_FEEDS:
    logger.warning("No JSON feeds are configured.")
else:
    for name, url in FeedConfig.JSON_FEEDS.items():
        downloader.download_json_feed(name, url)