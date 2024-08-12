"""Multicolor image."""

import random

from .formats import multicolor
from .scrtypes import MultiColorScreen


class MultiColorImage:
    """Multicolor image."""

    def __init__(self, bitmap: bytes,   # pylint: disable=too-many-arguments
                 screen: bytes, colors: bytes, bgcolor: bytes,
                 border: bytes) -> None:
        assert len(bitmap) == 8000
        assert len(screen) == 1000
        assert len(colors) == 1000
        assert len(bgcolor) == 1
        assert len(border) == 1
        assert ord(bgcolor) < 16
        assert ord(border) < 16
        self._image = MultiColorScreen(bitmap, screen, colors, bgcolor, border)

    def as_amica(self) -> bytes:
        """Export image in Amica Paint format."""
        return multicolor.ami.pack(self._image)

    def as_artist64(self) -> bytes:
        """Export image in Artist 64 format."""
        return multicolor.a64.pack(self._image)

    def as_artstudio(self) -> bytes:
        """Export image in Advanced Art Studio (OCP Art Studio) format."""
        return multicolor.art.pack(self._image)

    def as_cheese(self) -> bytes:
        """Export image in Cheese Paint format."""
        return multicolor.che.pack(self._image)

    def as_drp(self) -> bytes:
        """Export image in Draz Paint (compressed) format."""
        return multicolor.drp.pack(self._image)

    def as_drz(self) -> bytes:
        """Export image in Draz Paint (uncompressed) format."""
        return multicolor.drz.pack(self._image)

    def as_graphic_assault_system(self) -> bytes:
        """Export image in Graphic Assault System format."""
        return multicolor.gas.pack(self._image)

    def as_koala(self) -> bytes:
        """Export image in Koala Painter format."""
        return multicolor.koa.pack(self._image)

    def as_vidcom64(self) -> bytes:
        """Export image in Vidcom 64 format."""
        return multicolor.vid.pack(self._image)

    def as_zoomatic(self, escval: int = -1) -> bytes:
        """Export image in Zoomatic format."""
        return multicolor.zom.pack(self._image, escval=escval)

# ------------------------------------------------------------------------- #
# Black image                                                               #
# ------------------------------------------------------------------------- #


class BlackMultiC64(MultiColorImage):
    """Black multicolor image."""
    def __init__(self) -> None:
        bitmap = b'\x00' * 8000
        screen = b'\x00' * 1000
        colors = b'\x00' * 1000
        bgcolor = b'\x00'
        border = b'\x00'
        super().__init__(bitmap, screen, colors, bgcolor, border)

# ------------------------------------------------------------------------- #
# White image                                                               #
# ------------------------------------------------------------------------- #


class WhiteMultiC64(MultiColorImage):
    """White multicolor image."""
    def __init__(self) -> None:
        bitmap = b'\x11' * 8000
        screen = b'\x11' * 1000
        colors = b'\x11' * 1000
        bgcolor = b'\x01'
        border = b'\x01'
        super().__init__(bitmap, screen, colors, bgcolor, border)

# ------------------------------------------------------------------------- #
# Random image                                                              #
# ------------------------------------------------------------------------- #


class RandomMultiC64(MultiColorImage):
    """Random multicolor image."""
    def __init__(self) -> None:
        bitmap = random.randbytes(8000)
        screen = random.randbytes(1000)
        colors = random.randbytes(1000)
        bgcolor = random.randrange(15).to_bytes()
        border = random.randrange(15).to_bytes()
        super().__init__(bitmap, screen, colors, bgcolor, border)

# vim: set sts=4 et sw=4:
