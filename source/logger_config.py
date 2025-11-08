"""
Logging configuration for Accessible YouTube Downloader Pro
"""
import logging
import os
from datetime import datetime
from paths import settings_path

def setup_logging():
    """
    Set up logging configuration for the application.
    Logs are saved to the settings directory.
    """
    # Create logs directory
    log_dir = os.path.join(settings_path, "logs")
    try:
        os.makedirs(log_dir, exist_ok=True)
    except Exception as e:
        print(f"Could not create logs directory: {e}")
        return
    
    # Create log filename with timestamp
    log_filename = datetime.now().strftime("app_%Y%m%d.log")
    log_path = os.path.join(log_dir, log_filename)
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        handlers=[
            logging.FileHandler(log_path, encoding='utf-8'),
            logging.StreamHandler()  # Also print to console
        ]
    )
    
    # Set third-party loggers to WARNING to reduce noise
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    
    logger = logging.getLogger(__name__)
    logger.info("=" * 70)
    logger.info("Application started")
    logger.info(f"Log file: {log_path}")
    logger.info("=" * 70)
    
    return logger

def get_logger(name):
    """Get a logger instance for a specific module"""
    return logging.getLogger(name)
