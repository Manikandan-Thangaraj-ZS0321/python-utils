import logging
import os
from datetime import date

today = str(date.today())

LOG_SET_LEVEL = 'INFO'
LOG_FORMAT = "%(asctime)s %(process)d [%(levelname)s] [%(threadName)s] %(thread)d %(filename)s: %(lineno)s: %(message)s"
COPRO_LOG = f'logs/copro_process_{today}.log'

# Create the logs directory if it doesn't exist
log_directory = os.path.dirname(COPRO_LOG)
os.makedirs(log_directory, exist_ok=True)

# Set up the logger to log to both file and console
logging.basicConfig(filename=COPRO_LOG, format=LOG_FORMAT, level=logging.INFO)

# Add a StreamHandler to the root logger to also log to the console
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
logging.getLogger().addHandler(console_handler)

# Set the log level
logging.getLogger().setLevel(LOG_SET_LEVEL)

logger = logging.getLogger(__name__)
