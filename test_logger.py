from utils.logger import get_logger

logger = get_logger(__name__)

logger.info("Application started")
logger.warning("This is a warning")
logger.error("This is an error")