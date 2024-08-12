# pylint: disable=duplicate-code,too-many-arguments
"""Koala Painter."""

from ...scrtypes import MultiColorScreen

LDADDR = b'\x00\x60'

FILE_SIZE = 10_003


def pack(image: MultiColorScreen, _verbose: bool = False) -> bytes:
    """Koala Painter."""
    data = b''.join([
        LDADDR,
        image.bitmap,
        image.screen,
        image.colors,
        image.bgcolor
    ])

    assert len(data) == FILE_SIZE

    return data

# vim: set sts=4 et sw=4:
