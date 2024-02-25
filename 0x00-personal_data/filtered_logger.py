#!/usr/bin/env python3
"""
0. Regex-ing
"""
import re
from typing import List
import logging
import os
import mysql.connector


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """A function that returns an ambiguous log message."""
    pattern = "|".join(fields)
    return re.sub(f"({pattern})=[^{separator}]+", f"\\1={redaction}", message)


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """A function that takes no arguments
    and returns a logging.Logger object."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    formatter = RedactingFormatter(fields=PII_FIELDS)
    logger.addHandler(logging.StreamHandler().setFormatter(formatter))
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    "A function that returns a connector to the database"
    db_config = {
        "user": os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        "password": os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        "host": os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        "database": os.getenv("PERSONAL_DATA_DB_NAME")
    }
    try:
        return mysql.connector.connect(**db_config)
    except mysql.connector.Error:
        return None


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record, redacting sensitive information."""
        for field in self.fields:
            record.msg = re.sub(f"{field}=[^;]+",
                                f"{field}={self.REDACTION}", record.msg)
        return super().format(record)
