#!/usr/bin/env python3
"""CIA snapshot module."""

# https://www.c64-wiki.com/wiki/Sprite
# https://www.c64-wiki.com/wiki/Page_208-211
# https://sta.c64.org/cbm64mem.html

from .generic import VSFModule


class CIA2:
    """CIA snapshot module."""

    def __init__(self, mod: VSFModule):
        self.mod = mod
        self.payload = mod.payload

    @property
    def dd00(self) -> int:
        """VIC bank ($dd00).
        https://www.c64-wiki.com/wiki/VIC_bank
        """
        return self.payload[0x00]

    @property
    def vic_bank_addr(self) -> int:
        """VIC bank address (0x0000, 0x4000, 0x8000 or 0xc000)."""
        return 0xc000 - 0x4000 * (self.dd00 & 0b0000_0011)

    def version(self) -> str:
        """Return module version."""
        return self.mod.version()

    def __str__(self) -> str:
        return ', '.join([
            f'{self.__class__.__name__}(start=0x{self.mod.start_pos:x}, size={self.mod.size:_}',
            f'ver={self.mod.version()})'
        ])


# vim: set sts=4 et sw=4:
