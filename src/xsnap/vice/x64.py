"""X64."""

# from pathlib import Path

from .vsf import ViceSnapshotFile
# from .vsf.vic2 import GraphicsMode
# from ..utils import log


class X64:
    """X64."""

    def __init__(self, snap: ViceSnapshotFile):
        self.mem = snap.c64mem()
        self.cia2 = snap.cia2()
        self.vic2 = snap.vic2()

    # XXX:
    # def graphics_mode(self) -> GraphicsMode:
    #     """Return active screen graphics mode."""
    #     return self.vic2.graphics_mode()

    def has_active_sprites(self) -> bool:
        """Return True is the snapshot has active sprite(s)."""
        return self.vic2.has_active_sprites()

    def is_screen_hires(self) -> bool:
        """Return True if active screen is in hires mode."""
        # return self.vic2.graphics_mode() == GraphicsMode.MULTICOLOR
        return self.vic2.graphics_mode().is_hires_bitmap()

    def is_screen_multicolor(self) -> bool:
        """Return True if active screen is in multicolor mode."""
        # return self.vic2.graphics_mode() == GraphicsMode.MULTICOLOR
        return self.vic2.graphics_mode().is_multicolor_bitmap()

    def is_screen_text(self) -> bool:
        """Return True if active screen is in text mode."""
        # return self.vic2.graphics_mode() == GraphicsMode.MULTICOLOR
        return self.vic2.graphics_mode().is_standard_character()

    def bitmap_ram(self) -> memoryview:
        """Return Bitmap RAM."""
        bitmap_addr = self.cia2.vic_bank_addr + \
            8192 * ((self.vic2.d018 >> 3) & 1)
        return self.mem.ram(bitmap_addr, 8000)

    def color_ram(self) -> memoryview:
        """Return Color RAM."""
        return self.vic2.color_ram()

    def screen_ram(self) -> memoryview:
        """Return Screen RAM."""
        screen_addr = self.cia2.vic_bank_addr + \
            1024 * (self.vic2.d018 >> 4)
        return self.mem.ram(screen_addr, 1000)

    def background_color(self) -> bytes:
        """Return background color."""
        return self.vic2.background_color.to_bytes(1)

    def border_color(self) -> bytes:
        """Return border color."""
        return self.vic2.border_color.to_bytes(1)

    def memory_setup_register(self) -> bytes:
        """Return memory setup register value ($d018)."""
        return self.vic2.memory_setup_register.to_bytes(1)

    def show_info(self) -> None:
        """Show snapshot information."""
        print('X64 snapshot modules:')
        print('   Module C64MEM version', self.mem.version())
        print('   Module CIA2   version', self.cia2.version())
        print('   Module VIC2   version', self.vic2.version())
        self.vic2.info(self.cia2.dd00)
        # return
        # print('CIA2 Registers:')
        # print(f'   CIA2  : $dd00 = ${self.cia2.dd00:02x} (%{self.cia2.dd00:08b})')

    #     else:
    #         print('\033[93mW: No export formats defined for', mode, 'graphics mode\033[0m')


# vim: set sts=4 et sw=4:
