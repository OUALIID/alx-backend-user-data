#!/usr/bin/env python3
"""
0. Regex-ing
"""
import re


def filter_datum(fields, redaction, message, separator):
    """A function that returns an ambiguous log message."""
    pattern = "|".join(fields)
    return re.sub(f"({pattern})=[^;]+", f"\\1={redaction}", message)
