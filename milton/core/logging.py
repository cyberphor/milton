"""Defining logging."""

# Standard library imports.
from json import dumps
from logging import DEBUG, Formatter, getLogger, StreamHandler


class JSONFormatter(Formatter):
    def format(self, event):
        log = {
            "timestamp": self.formatTime(event),
            "name": event.name,
            "level": event.levelname,
            "message": event.getMessage(),
        }
        return dumps(log)
    
def get_logger(name: str):
    # Init a logger.
    logger = getLogger(name)

    # Set the default logging level.
    logger.setLevel(level=DEBUG)

    # Init a stream handler.
    handler = StreamHandler()

    # Init a formatter.
    formatter = JSONFormatter()
    
    # Attach the formatter to the handler.
    handler.setFormatter(formatter)

    # Attach the handler to the logger.
    logger.addHandler(handler)

    return logger
