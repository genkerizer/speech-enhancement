import logging
from datetime import datetime
import os


class Logger():

    def __init__(self):
        self.relative_path = os.path.dirname(os.path.realpath(__file__))
        self.root_log_dir = os.path.join(self.relative_path, "logs")
        if not os.path.exists(self.root_log_dir):
            os.makedirs(self.root_log_dir)

    def check_log_dir(self):
        today = datetime.now()
        log_path = os.path.join(self.root_log_dir, today.strftime("%Y/%m/%d"))
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        log_file = os.path.join(log_path, "".join(today.strftime("%Y-%m-%d")) + ".log")
        logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        
    def log_info(self, message):
        self.check_log_dir()
        logging.info(message)

    def log_debug(self, message):
        self.check_log_dir()
        logging.debug(message)

    def log_warning(self, message):
        self.check_log_dir()
        logging.warning(message)

    def log_exception(self, message):
        self.check_log_dir()
        logging.exception(message)

logger = Logger()

