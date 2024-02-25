#!/usr/bin/env python3
"""
0. Regex-ing
"""


def filter_datum(fields, redaction, message, separator):
    """A function that returns an ambiguous log message."""
    for pair in message.split(separator):
        key, value = pair.split('=', 1) if '=' in pair else (None, None)
        if key in fields:
            message = message.replace(pair, f"{key}={redaction}")
    return message
