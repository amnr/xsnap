# pylint: disable=duplicate-code,too-many-arguments
"""HiPic Creator."""

from ...scrtypes import HiresScreen

LDADDR = b'\x00\x60'

FILE_SIZE = 9003


def pack(image: HiresScreen, _verbose: bool = False) -> bytes:
    """HiPic Creator."""
    data = b''.join([
        LDADDR,
        image.bitmap,
        image.screen,
        image.border
    ])

    assert len(data) == FILE_SIZE

    return data

# vim: set sts=4 et sw=4:
