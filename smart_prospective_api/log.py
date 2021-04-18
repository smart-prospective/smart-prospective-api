from .string import str_to_ascii


class Log:
    """
    This class override logging system to fix encoding problem.

    :param string logger_name: The logger name, define in settings.
    """
    logger = None

    def __init__(self, logger_name):
        import logging
        self.logger_name = logger_name
        self.logger = logging.getLogger(logger_name)

    def debug(self, msg):
        """
        Add a log message level 'debug'.

        :param string msg: Message to log
        """
        try:
            self.logger.debug(f"{msg}")
        except:
            self.logger.warning("Error logging format!")
            self.logger.debug(str_to_ascii(f"{msg}"))

    def info(self, msg):
        """
        Add a log message level 'info'.

        :param string msg: Message to log
        """
        try:
            self.logger.info(f"{msg}")
        except:
            self.logger.warning("Error logging format!")
            self.logger.info(str_to_ascii(f"{msg}"))

    def warning(self, msg):
        """
        Add a log message level 'warning'.

        :param string msg: Message to log
        """
        try:
            self.logger.warning(f"{msg}")
        except:
            self.logger.warning("Error logging format!")
            self.logger.warning(str_to_ascii(f"{msg}"))

    def error(self, msg):
        """
        Add a log message level 'error'.

        :param string msg: Message to log
        """
        try:
            self.logger.error(f"{msg}")
        except:
            self.logger.warning("Error logging format!")
            self.logger.error(str_to_ascii(f"{msg}"))

    def critical(self, msg):
        """
        Add a log message level 'critical'.

        :param string msg: Message to log
        """
        try:
            self.logger.critical(f"{msg}")
        except:
            self.logger.warning("Error logging format!")
            self.logger.critical(str_to_ascii(f"{msg}"))


def getLogger():
    """
    This function generate a Log object
    """
    return Log("smart-prospective-api")
