#!/usr/bin/env python3
"""
0. Regex-ing
"""
import re
from typing import List
import logging


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """A function that returns an ambiguous log message."""
    pattern = "|".join(fields)
    return re.sub(f"({pattern})=[^{separator}]+", f"\\1={redaction}", message)


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
