#!/usr/bin/env python3
'''logging by hiding secure data'''
import re
import logging
import os
from typing import List
from mysql.connector.connection import MySQLConnection


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str], redaction: str,
        message: str, separator: str) -> str:
    '''filter data'''
    for field in fields:
        message = re.sub(f"{field}=[^;]*", rf"{field}={redaction}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]) -> None:
        '''initializing the formatter'''
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        '''formatting logs'''
        return filter_datum(self.fields, self.REDACTION,
                                super().format(record), self.SEPARATOR)


def get_logger() -> logging.Logger:
    '''
        returns Logger object with userdata name
        info level with RedactingFormatter formatter
    '''
    logger = logging.getLogger(name="user_data")
    logger.selevel = logging.INFO
    logger.propagate = False
    handler = logging.ha
    return logger


def get_db():
    '''connects to database and return a connector object'''
    user = os.getenv("PERSONAL_DATA_DB_USERNAME") or "root"
    passwd = os.getenv("PERSONAL_DATA_DB_PASSWORD") or ""
    host = os.getenv("PERSONAL_DATA_DB_HOST") or "localhost"
    db = os.getenv("PERSONAL_DATA_DB_NAME")

    try:
        conn = MySQLConnection(
            user=user, passwd=passwd,
            host=host, db=db
        )
    except Exception as e:
        print("Error connecting to db", e)
        exit(1)

    return conn


def main():
    '''excution starts here'''
    conn = get_db()

    cursor = conn.cursor()
    sql = "SELECT * FROM users"
    cursor.execute(sql)
    logger = get_logger()
    for row in cursor:
        record = logging.LogRecord(exc_info=row)
        print(logger.format())
        print(row)

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
