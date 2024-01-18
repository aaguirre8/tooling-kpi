import os
import logging
from logging.handlers import RotatingFileHandler

class Logger:
    """
    Logger class for application-wide logging.

    Attributes:
        logger_name (str): Name of the logger.
    """

    def __init__(self, logger_name: str, log_file: str = 'app.log'):
        self.logger_name = logger_name

        # Create a custom logger
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)  # Set the logging level

        # Create handlers
        c_handler = logging.StreamHandler()  # Console handler
        f_handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=5)  # File handler

        # Create formatters and add it to handlers
        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        # Add handlers to the logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

        self.logger = logger

    def get_logger(self):
        return self.logger
