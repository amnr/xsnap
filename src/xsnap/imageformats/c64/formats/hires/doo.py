# pylint: disable=duplicate-code,too-many-arguments
"""Doodle!."""

from ...scrtypes import HiresScreen

LDADDR = b'\x00\x5c'

FILE_SIZE = 9218


def pack(image: HiresScreen, _verbose: bool = False) -> bytes:
    """Doodle!."""
    data = b''.join([
        LDADDR,
        image.screen,
        bytes(24),
        image.bitmap,
        bytes(192)
    ])

    assert len(data) == FILE_SIZE

    return data

# vim: set sts=4 et sw=4:
