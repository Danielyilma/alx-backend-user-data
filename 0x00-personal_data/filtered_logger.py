#!/usr/bin/env python3
'''logging by hiding secure data'''
import re
import logging
import os
from typing import List
from mysql.connector.connection import MySQLConnection


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    '''filter data'''
    for field in fields:
        message = re.sub(f"{field}=.*?{separator}",
                         rf"{field}={redaction}{separator}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        '''initializing the formatter'''
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''formatting logs'''
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)
