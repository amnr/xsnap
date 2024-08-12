# pylint: disable=duplicate-code,too-many-arguments
"""Art Studio Hires."""

from ...scrtypes import HiresScreen

LDADDR = b'\x00\x20'

FILE_SIZE = 9009


def pack(image: HiresScreen, _verbose: bool = False) -> bytes:
    """Art Studio Hires."""
    data = b''.join([
        LDADDR,
        image.bitmap,
        image.screen,
        image.border,
        bytes(6)
    ])

    assert len(data) == FILE_SIZE

    return data

# vim: set sts=4 et sw=4:
