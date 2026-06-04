import logging
import time

class Logger:
    def __init__(self, path: str, loggingEnabled: bool):
        self.path = path
        self.loggingEnabled = loggingEnabled

        self.lastLogTime = time.time()
        self.startTime   = time.time()

        if self.loggingEnabled:
            logging.basicConfig(filename=path,      filemode="w",
                                level=logging.INFO, format="%(asctime)s - %(message)s")
        
    def timeLog(self, message: str):
        logTime = time.time()
        logDeltaTime = logTime - self.lastLogTime
        logDeltaTimeMS = int(logDeltaTime * 1000)
        self.lastLogTime = logTime

        if self.loggingEnabled:
            logging.info(f"+{logDeltaTimeMS:04d} ms - {message}")
    
    def log(self, message: str):
        if self.loggingEnabled:
            logging.info(f"{message}")
        
    def blankLine(self):
        if self.loggingEnabled:
            for handler in logging.root.handlers:
                if isinstance(handler, logging.FileHandler):
                    handler.stream.write("\n")
                    handler.stream.flush()
                    break