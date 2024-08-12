#!/usr/bin/env python3
"""Log utils."""

from datetime import datetime
from typing import Any


def debug(*text: Any) -> None:
    """Show debug message."""
    print('\033[1;35m', datetime.now(), '  \033[1;30mDEBUG\033[0m  ', end='', sep='')
    print(*text)


def error(*text: Any) -> None:
    """Show error message."""
    print('\033[1;31mError:', *text, end='')
    print('\033[0m')


def info(*text: Any) -> None:
    """Show informational message."""
    print(*text)


def warn(*text: Any) -> None:
    """Show warning message."""
    # print('\033[1;35m', datetime.now(), '  \033[1;33mWARN \033[0m  ', end='', sep='')
    # print('\033[1;35m', datetime.now(), '  \033[1;33mWARN \033[0m  ', end='', sep='')
    # print(*text)
    print('\033[93mWarning:', *text, end='')
    print('\033[0m')


# vim: set sts=4 et sw=4:
