"""Text image."""

import random

from .formats import text
from .scrtypes import TextScreen


class TextImage:
    """Text image."""

    def __init__(self, screen: bytes,   # pylint: disable=too-many-arguments
                 colors: bytes, bgcolor: bytes, border: bytes,
                 d018: bytes = b'\x00') -> None:
        assert len(screen) == 1000
        assert len(colors) == 1000
        assert len(bgcolor) == 1
        assert len(border) == 1
        assert len(d018) == 1       # XXX: check values.
        assert ord(bgcolor) < 16
        assert ord(border) < 16
        self._image = TextScreen(screen, colors, bgcolor, border, d018)

    def as_pdr(self) -> bytes:
        """Export image in Petdraw64 format."""
        return text.pdr.pack(self._image)

    def as_pet(self) -> bytes:
        """Export image in PETSCII Editor format."""
        return text.pet.pack(self._image)

# ------------------------------------------------------------------------- #
# Black image                                                               #
# ------------------------------------------------------------------------- #


class BlackTextC64(TextImage):
    """Black text image."""
    def __init__(self) -> None:
        screen = b'\x00' * 1000
        colors = b'\x00' * 1000
        bgcolor = b'\x00'
        border = b'\x00'
        d018 = b'\x00'      # XXX: TODO.
        super().__init__(screen, colors, bgcolor, border, d018)

# ------------------------------------------------------------------------- #
# White image                                                               #
# ------------------------------------------------------------------------- #


class WhiteTextC64(TextImage):
    """White text image."""
    def __init__(self) -> None:
        screen = b'\x11' * 1000
        colors = b'\x11' * 1000
        bgcolor = b'\x01'
        border = b'\x01'
        d018 = b'\x00'      # XXX: TODO.
        super().__init__(screen, colors, bgcolor, border, d018)

# ------------------------------------------------------------------------- #
# Random image                                                              #
# ------------------------------------------------------------------------- #


class RandomTextC64(TextImage):
    """Random text image."""
    def __init__(self) -> None:
        screen = random.randbytes(1000)
        colors = random.randbytes(1000)
        bgcolor = random.randrange(15).to_bytes()
        border = random.randrange(15).to_bytes()
        d018 = b'\x00'      # XXX: TODO.
        super().__init__(screen, colors, bgcolor, border, d018)

# vim: set sts=4 et sw=4:
