"""Pack library."""

from dataclasses import dataclass


@dataclass
class HiresScreen:
    """Hires screen data."""
    bitmap: bytes
    screen: bytes
    border: bytes = b'\x00'


@dataclass
class MultiColorScreen:
    """Multicolor screen data."""
    bitmap: bytes
    screen: bytes
    colors: bytes
    bgcolor: bytes
    border: bytes = b'\x00'


@dataclass
class TextScreen:
    """Text screen data."""
    screen: bytes
    colors: bytes
    bgcolor: bytes
    border: bytes
    d018: bytes = b'\x00'       # VIC-II memory control register.

# vim: set sts=4 et sw=4:
