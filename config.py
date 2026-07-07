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
    """Threat feed definations."""

    JSON_FEEDS = {}
    