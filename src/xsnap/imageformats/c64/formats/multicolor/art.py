# pylint: disable=duplicate-code,too-many-arguments
"""Advanced Art Studio (OCP Art Studio)."""

from ...scrtypes import MultiColorScreen

LDADDR = b'\x00\x20'

FILE_SIZE = 10_018


def pack(image: MultiColorScreen, _verbose: bool = False) -> bytes:
    """Advanced Art Studio (OCP Art Studio)."""
    data = b''.join([
        LDADDR,
        image.bitmap,
        image.screen,
        image.border,
        image.bgcolor,
        bytes(14),
        image.colors
    ])

    assert len(data) == FILE_SIZE

    return data

# vim: set sts=4 et sw=4:
