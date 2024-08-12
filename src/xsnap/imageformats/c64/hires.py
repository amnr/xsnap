"""Hires image."""

import random

from .formats import hires
from .scrtypes import HiresScreen


class HiresImage:
    """Hires image."""

    def __init__(self, bitmap: bytes, screen: bytes, border: bytes = b'\x00') -> None:
        assert len(bitmap) == 8000
        assert len(screen) == 1000
        assert len(border) == 1
        assert ord(border) < 16
        self._image = HiresScreen(bitmap, screen, border)

    def as_aas(self) -> bytes:
        """Export image in Art Studio Hires format."""
        return hires.aas.pack(self._image)

    def as_doo(self) -> bytes:
        """Export image in Doodle! format."""
        return hires.doo.pack(self._image)

    def as_hpc(self) -> bytes:
        """Export image in HiPic Creator format."""
        return hires.hpc.pack(self._image)

# ------------------------------------------------------------------------- #
# Black image                                                               #
# ------------------------------------------------------------------------- #


class BlackHiresC64(HiresImage):
    """Black hires image."""
    def __init__(self) -> None:
        bitmap = b'\x00' * 8000
        screen = b'\x00' * 1000
        border = b'\x00'
        super().__init__(bitmap, screen, border)

# ------------------------------------------------------------------------- #
# White image                                                               #
# ------------------------------------------------------------------------- #


class WhiteHiresC64(HiresImage):
    """White hires image."""
    def __init__(self) -> None:
        bitmap = b'\x11' * 8000
        screen = b'\x11' * 1000
        border = b'\x01'
        super().__init__(bitmap, screen, border)

# ------------------------------------------------------------------------- #
# Random image                                                              #
# ------------------------------------------------------------------------- #


class RandomHiresC64(HiresImage):
    """Random hires image."""
    def __init__(self) -> None:
        bitmap = random.randbytes(8000)
        screen = random.randbytes(1000)
        border = random.randrange(15).to_bytes()
        super().__init__(bitmap, screen, border)

# vim: set sts=4 et sw=4:
