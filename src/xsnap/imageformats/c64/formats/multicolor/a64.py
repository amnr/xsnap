# pylint: disable=duplicate-code,too-many-arguments
"""Artist 64."""

from ...scrtypes import MultiColorScreen

# Load address.
LDADDR = b'\x00\x40'

FILE_SIZE = 10_242


def pack(image: MultiColorScreen, _verbose: bool = False) -> bytes:
    """Artist 64."""
    data = b''.join([
        LDADDR,
        image.bitmap,
        bytes(192),
        image.screen,
        bytes(24),
        image.colors,
        bytes(23),
        image.bgcolor
    ])

    assert len(data) == FILE_SIZE

    return data

# vim: set sts=4 et sw=4:
