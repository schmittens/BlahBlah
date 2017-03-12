import logging
from datetime import datetime

class SRLogger:
    def __init__(self):
        self.filetime = datetime.now()
        self.filetime_format = "%Y%m%d-%H%M%S"

        fname = self.filetime.strftime(self.filetime_format) + ".txt"
        fpath = "logs/"
        self.filename = fpath + fname

        #self.logging = logging.basicConfig(filename=self.filename,level=logging.DEBUG)
        logging.basicConfig(filename=self.filename,level=logging.DEBUG)
        #self.logging.info("Starting log")
        logging.info("Starting log")

    def addDebug(message):
        logging.debug(message)
        return True


    def addInfo(message):
        logging.info(message)
        return True


    def addWarning(message):
        logging.warning(message)
        return True