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
                    else "./"
        self.current_datetime = datetime.now(timezone.utc)
        self.FORMAT = "%(asctime)-15s %(levelname)s %(message)s"
        self.FILEMODE = "a"

    def set_error(self, message: str, log_file: str = "api_run"):
        """log errors
        """
        LOGFILE = self.logging_folder + "/" + log_file + "_" \
                        + self.current_datetime.strftime("%Y%m%d") + ".log"
        logging.basicConfig(format=self.FORMAT, level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    filename = LOGFILE, filemode = self.FILEMODE)
        logging.error(message)

        print(LOGFILE)

    def set_info(self, message: str, log_file: str = "api_run"):
        """log errors
        """
        LOGFILE = self.logging_folder + "/" + log_file + "_" \
                        + self.current_datetime.strftime("%Y%m%d") + ".log"
        logging.basicConfig(format=self.FORMAT, level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    filename = LOGFILE, filemode = self.FILEMODE)
        logging.info(message)

    def set_warning(self, message: str,):
        """log warnings
        """
        current_datetime = datetime.now(timezone.utc)
        logging.warning(current_datetime.strftime("%Y-%m-%d %H:%M:%S"))
        logging.warning(message)
