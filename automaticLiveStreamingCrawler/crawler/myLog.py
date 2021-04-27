#myLog.py
import logging
import logging.handlers
import re

class MyLog(object):
    def __init__(self, user):
        self.logger=logging.getLogger(user)
        self.logger.setLevel(logging.DEBUG)
        format='%(asctime)s - %(levelname)s -%(name)s : %(message)s'
        formatter=logging.Formatter(format)
        #streamhandler=logging.StreamHandler()
        #streamhandler.setFormatter(formatter)
        #self.logger.addHandler(streamhandler)
        logfile='./' + user
        filehandler=logging.FileHandler(logfile)
        filehandler = logging.handlers.TimedRotatingFileHandler(filename=logfile, when="D", interval=1, backupCount=7)
        filehandler.suffix = "%Y-%m-%d_%H:%M.log"
        filehandler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}:\d{2}.log$")
        filehandler.setFormatter(formatter)
        self.logger.addHandler(filehandler)
    def debug(self, msg):
        self.logger.debug(msg)
    def info(self, msg):
        self.logger.info(msg)
    def warning(self, msg):
        self.logger.warning(msg)
    def error(self, msg):
        self.logger.error(msg)
    def critical(self, msg):
        self.logger.critical(msg)
    def log(self, level, msg):
        self.logger.log(level, msg)
    def setLevel(self, level):
        self.logger.setLevel(level)
    def disable(self):
        logging.disable(50)

#http://yhhuang1966.blogspot.com/2018/04/python-logging_24.html
#https://blog.csdn.net/energysober/article/details/53263295
#http://pythonfans.lofter.com/post/3dd906_68774a3