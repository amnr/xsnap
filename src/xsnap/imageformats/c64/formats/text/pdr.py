# pylint: disable=duplicate-code,too-many-arguments
"""Petdraw64."""

from ...scrtypes import TextScreen

LDADDR = b'\x71\x31'

FILE_SIZE = 2029


def pack(image: TextScreen, _verbose: bool = False) -> bytes:
    """Petdraw64."""
    data = b''.join([
        LDADDR,
        b'\x01',        # Active foreground color (selected by user).
        image.bgcolor,
        image.border,
        image.screen,
        bytes(24),
        image.colors
    ])

    assert len(data) == FILE_SIZE

    return data

# vim: set sts=4 et sw=4:
