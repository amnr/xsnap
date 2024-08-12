# pylint: disable=duplicate-code,too-many-arguments
"""Draz Paint (uncompressed)."""

from ...scrtypes import MultiColorScreen

LDADDR = b'\x00\x58'

FILE_SIZE = 10_051


def pack(image: MultiColorScreen, _verbose: bool = False) -> bytes:
    """Draz Paint (uncompressed)."""
    data = b''.join([
        LDADDR,
        image.colors,
        bytes(24),
        image.screen,
        bytes(24),
        image.bitmap,
        image.bgcolor
    ])

    assert len(data) == FILE_SIZE

    return data

# vim: set sts=4 et sw=4:
