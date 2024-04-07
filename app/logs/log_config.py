import structlog
import logging
from datetime import date
import os

structlog.configure(
    processors=[
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)

log_file = f"logs/app_{date.today()}.log"

# Create a file handler to log messages to the file
file_handler = logging.FileHandler(log_file)

# Define a custom formatter that includes only the file name and lineno
file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - [%(pathname)s:%(lineno)d] - %(message)s")
file_handler.setFormatter(file_formatter)

# Create a console handler to log messages to the console (stdout)
console_handler = logging.StreamHandler()

# Define a custom formatter for the console with only the file name
console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - [%(pathname)s:%(lineno)d] - %(message)s")
console_handler.setFormatter(console_formatter)

# Get the root logger
root_logger = logging.getLogger()

# Add both file and console handlers to the root logger
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)
root_logger.setLevel(logging.INFO)


# Create the structlog logger
logger = structlog.get_logger()
