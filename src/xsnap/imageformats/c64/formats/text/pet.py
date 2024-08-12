# pylint: disable=duplicate-code,too-many-arguments
"""PETSCII Editor."""

from ...scrtypes import TextScreen

LDADDR = b'\x00\x30'

FILE_SIZE = 2026


def pack(image: TextScreen, _verbose: bool = False) -> bytes:
    """PETSCII Editor."""
    data = b''.join([
        LDADDR,
        image.screen,
        image.border,
        image.bgcolor,
        image.d018,
        bytes(21),
        image.colors
    ])

    assert len(data) == FILE_SIZE

    return data

# vim: set sts=4 et sw=4:
