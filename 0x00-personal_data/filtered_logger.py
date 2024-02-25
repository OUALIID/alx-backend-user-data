#!/usr/bin/env python3
"""
0. Regex-ing
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """A function that returns an ambiguous log message."""
    pattern = "|".join(fields)
    return re.sub(f"({pattern})=[^;]+", f"\\1={redaction}", message)
