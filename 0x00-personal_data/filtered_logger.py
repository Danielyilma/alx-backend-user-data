#!/usr/bin/env python3
'''logging by hiding secure data'''
import re
import logging


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
