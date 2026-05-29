import logging
import time

class Logger:
    def __init__(self, path: str, loggingEnabled: bool):
        self.lastLogTime = time.time()
        self.loggingEnabled = loggingEnabled

        if self.loggingEnabled:
            logging.basicConfig(filename=path,      filemode="w",
                                level=logging.INFO, format="%(asctime)s - %(message)s")
        
    def log(self, message: str):
        logTime = time.time()
        logDeltaTime = logTime - self.lastLogTime
        logDeltaTimeMS = int(logDeltaTime * 1000)
        self.lastLogTime = logTime

        if self.loggingEnabled:
            logging.info(f"+{logDeltaTimeMS:04d} ms - {message}")
        