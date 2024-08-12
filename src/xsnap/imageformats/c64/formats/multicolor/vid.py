# pylint: disable=duplicate-code,too-many-arguments
"""Vidcom 64."""

from ...scrtypes import MultiColorScreen

LDADDR = b'\x00\x58'

FILE_SIZE = 10_050


def pack(image: MultiColorScreen, _verbose: bool = False) -> bytes:
    """Vidcom 64."""
    data = b''.join([
        LDADDR,
        image.colors,
        bytes(24),
        image.screen,
        image.bgcolor,
        bytes(23),
        image.bitmap
    ])

    assert len(data) == FILE_SIZE

    return data

# vim: set sts=4 et sw=4:
