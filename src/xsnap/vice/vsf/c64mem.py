#!/usr/bin/env python3
"""C64 Memory module."""

# https://www.c64-wiki.com/wiki/Sprite
# https://www.c64-wiki.com/wiki/Page_208-211
# https://sta.c64.org/cbm64mem.html

from .generic import VSFModule

_C64MEM_MAGIC = b'C64MEM'


class C64Mem:
    """C64 Memory module."""

    def __init__(self, mod: VSFModule):
        assert mod.magic == _C64MEM_MAGIC
        self.mod = mod
        self._memory = self.mod.payload[4:4 + 65536]
        assert len(self._memory) == 65536

    def ram(self, start_addr: int, size: int) -> memoryview:
        """C64 RAM $0000 … $ffff."""
        result = self._memory[start_addr:start_addr + size]
        assert len(result) == size
        return result

    def version(self) -> str:
        """Return version string."""
        return self.mod.version()

    def __str__(self) -> str:
        return ', '.join([
            f'{self.__class__.__name__}(start=0x{self.mod.start_pos:x}, size={self.mod.size:_}',
            f'ver={self.mod.version()})'
        ])


# vim: set sts=4 et sw=4:
