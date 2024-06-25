import logging
from loguru import logger

def setup_logger():
    logging.basicConfig(level=logging.INFO)
    logger.add("oasis.log", rotation="1 day", retention="7 days", level="INFO")
    return logger

logger = setup_logger()
