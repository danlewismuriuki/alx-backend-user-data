#!/usr/bin/env python3
"""
Defines a logger with custom log formatter
"""
import os
import re
import logging
from typing import List, Tuple

# import mysql.connector


PII_FIELDS: Tuple[str] = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(
    fields: List[str], redaction: str,
    message: str, separator: str
) -> str:
    """
    Filters message by replacing each value in fields with redaction
    """
    for key in fields:
        pattern = r'({0}=)[^{1}]*({1})'.format(key, separator)
        message = re.sub(pattern, r'\1{}\2'.format(redaction), message)
    return message


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
        message = super().format(record)
        return filter_datum(
            self.fields,
            self.REDACTION,
            message,
            self.SEPARATOR)
