#!/usr/bin/env python3
'''logging by hiding secure data'''
import re
import logging


PII_FIELDS = ("name","email","phone","ssn","password")

def filter_datum(fields, redaction, message, separator):
    for field in fields:
        match = re.match(rf".*{field}=([^{separator}]+){separator}.*", message)
        message = re.sub(f"{match.group(1)}", redaction, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        ''''''
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        '''formatting logs'''
        record.msg = filter_datum(self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return logging.Formatter.format(self, record)


def get_logger() -> logging.Logger:
    '''
        returns Logger object with userdata name
        info level with RedactingFormatter formatter
    '''
    logger = logging.Logger(name="user_data", level=logging.INFO)
    logger.setStream()
    logger.propagate = False
    logger.setFormatter(RedactingFormatter(PII_FIELDS))
    return logger
