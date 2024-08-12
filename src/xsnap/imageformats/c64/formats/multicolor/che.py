# pylint: disable=duplicate-code,too-many-arguments
"""Cheese Paint."""

from ...scrtypes import MultiColorScreen

LDADDR = b'\x00\x80'

FILE_SIZE = 20_482


def pack(image: MultiColorScreen, _verbose: bool = False) -> bytes:
    """Cheese Paint."""
    data = b''.join([
        LDADDR,
        image.bitmap,
        bytes(8896),
        image.screen,
        bytes(536),
        image.colors,
        bytes(1045),
        image.bgcolor,
        bytes(2)
    ])

    assert len(data) == FILE_SIZE

    return data

# vim: set sts=4 et sw=4:
