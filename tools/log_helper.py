"""modules imports
"""
from datetime import datetime, timezone
import logging
import os
from dotenv import load_dotenv

class log_helper:
    """manage errors
    """
    def __init__(self):
        load_dotenv()
        self.logging_folder = os.getenv('LOGGING_FOLDER')\
                    if os.getenv('LOGGING_FOLDER') is not None\
                    else "."
        self.current_datetime = datetime.now(timezone.utc)
        self.format = "%(asctime)-15s %(levelname)s %(message)s"
        self.filemode = "a"

    def set_error(self, message: str, log_file: str = "api_run"):
        """log errors
        """
        logfile = self.logging_folder + "/" + log_file + "_" \
                        + self.current_datetime.strftime("%Y%m%d") + ".log"
        logging.basicConfig(format=self.format, level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    filename = logile, filemode = self.filemode)
        logging.error(message)

    def set_info(self, message: str, log_file: str = "api_run"):
        """log errors
        """
        logfile = self.logging_folder + "/" + log_file + "_" \
                        + self.current_datetime.strftime("%Y%m%d") + ".log"
        logging.basicConfig(format=self.format, level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    filename = logfile, filemode = self.filemode)
        logging.info(message)

    def set_warning(self, message: str,):
        """log warnings
        """
        current_datetime = datetime.now(timezone.utc)
        logging.warning(current_datetime.strftime("%Y-%m-%d %H:%M:%S"))
        logging.warning(message)
