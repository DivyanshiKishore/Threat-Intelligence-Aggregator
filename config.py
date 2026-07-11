from pathlib import Path


class ProjectConfig:
    """General project information."""

    PROJECT_NAME = "Threat Intelligence Aggregator"
    VERSION = "1.0.0"
    AUTHOR = "Divyanshi Kishore"


class PathConfig:
    """Project directory paths."""

    BASE_DIR = Path(__file__).resolve().parent

    FEEDS_DIR = BASE_DIR / "feeds"
    LOCAL_FEEDS_DIR = FEEDS_DIR / "local"
    REMOTE_FEEDS_DIR = FEEDS_DIR / "remote"

    LOGS_DIR = BASE_DIR / "logs"
    OUTPUT_DIR = BASE_DIR / "output"
    REPORTS_DIR = BASE_DIR / "reports"
    PDF_DIR = BASE_DIR / "pdf"


class NetworkConfig:
    """Network-related settings."""

    REQUEST_TIMEOUT = 10
    MAX_RETRIES = 3

    USER_AGENT = (
        "Threat-Intelligence-Aggregator/1.0 "
        "(Educational Project)"
    )


class LoggingConfig:
    """Logging configuration."""

    LOG_LEVEL = "INFO"
    LOG_FILE = "threat_intelligence.log"


class FeedConfig:
    """Threat intelligence feed configuration."""

    FEEDS = [
        {
            "name": "FireHOL",
            "type": "url",
            "format": "txt",
            "location": "https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/firehol_level1.netset",
        },
        {
            "name": "OpenPhish",
            "type": "url",
            "format": "txt",
            "location": "https://openphish.com/feed.txt",
        },
        {
            "name": "URLhaus",
            "type": "url",
            "format": "csv",
            "location": "https://urlhaus.abuse.ch/downloads/csv_recent/",
            "filename": "urlhaus.csv",
        },
        {
            "name": "Local TXT Sample",
            "type": "file",
            "format": "txt",
            "location": PathConfig.LOCAL_FEEDS_DIR / "sample.txt",
        },
        {
            "name": "Local CSV Sample",
            "type": "file",
            "format": "csv",
            "location": PathConfig.LOCAL_FEEDS_DIR / "sample.csv",
        },
        {
            "name": "Local JSON Sample",
            "type": "file",
            "format": "json",
            "location": PathConfig.LOCAL_FEEDS_DIR / "sample.json",
        },
    ]