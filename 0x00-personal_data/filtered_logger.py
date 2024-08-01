#!/usr/bin/env python3
'''Filter logs with regex'''
import re
from typing import List
import logging
import os
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''Filter and format values'''
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    '''Filter definition using Regex'''
    for f in fields:
        message = re.sub(f + "=.*?" + separator,
                         f + "=" + redaction + separator, message)
    return message


def get_logger() -> logging.Logger:
    '''Definition that takes no arguments
    and returns a logging.Logger object.'''
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = logging.Formatter(RedactingFormatter(PII_FIELDS))
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''Obtain te auth data from a env var'''
    connector = mysql.connector.connect(
        user=os.environ.get("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.environ.get("PERSONAL_DATA_DB_PASSWORD", ""),
        host=os.environ.get("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.environ.get("PERSONAL_DATA_DB_NAME"))
    return connector


if __name__ == '__main__':
    connection = get_db()
    cursor = connection.cursor(dictionary=True)
    query = ("SELECT * FROM users")
    cursor.execute(query)
    for row in cursor:
        string = ""
        for key in row:
            string += "{}={}; ".format(key, row[key])
        print(string)
    cursor.close()
    connection.close()