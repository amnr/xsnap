#!/usr/bin/env python3
"""VIC-II snapshot module."""

# https://www.c64-wiki.com/wiki/Sprite
# https://www.c64-wiki.com/wiki/Page_208-211
# https://sta.c64.org/cbm64mem.html

from dataclasses import dataclass
from enum import Enum

from .generic import VSFModule


COLOR_NAME = (
    'black', 'white', 'red', 'cyan',
    'purple', 'green', 'blue', 'yellow',
    'orange', 'brown', 'pink', 'dark grey',
    'grey', 'light green', 'light blue', 'light grey'
)


VIC_REG_OFFSET = 1119


class GraphicsMode(Enum):
    """VIC-II graphics mode."""
    CHAR_STD = 0
    CHAR_MULTI = 1
    BITMAP = 2
    MULTICOLOR = 3
    EXT_BGCOL = 4
    INVALID_5 = 5
    INVALID_6 = 6
    INVALID_7 = 7

    def is_standard_character(self) -> bool:
        """Return True if graphics mode is standard character."""
        return self.value == GraphicsMode.CHAR_STD.value

    def is_hires_bitmap(self) -> bool:
        """Return True if graphics mode is hires bitmap."""
        return bool(self.value == GraphicsMode.BITMAP.value)

    def is_multicolor_bitmap(self) -> bool:
        """Return True if graphics mode is multicolor bitmap."""
        return bool(self.value == GraphicsMode.MULTICOLOR.value)

    def __str__(self) -> str:
        if self.value == GraphicsMode.CHAR_STD.value:
            return 'standard character'
        if self.value == GraphicsMode.CHAR_MULTI.value:
            return 'multicolor character'
        if self.value == GraphicsMode.BITMAP.value:
            return 'hires bitmap'
        if self.value == GraphicsMode.MULTICOLOR.value:
            return 'multicolor bitmap'
        if self.value == GraphicsMode.EXT_BGCOL.value:
            return 'extended background color character'
        return f'(invalid: {self.value})'


@dataclass
class Sprite:           # pylint: disable=too-many-instance-attributes
    """Sprite."""

    num: int
    status: bool
    posx: int
    posy: int
    multicolor: bool
    color01: int
    color10: int
    color11: int
    xexp: bool
    yexp: bool

    @property
    def exp(self) -> str:
        """@@@"""
        xmul = 2 if self.xexp else 1
        ymul = 2 if self.yexp else 1
        return f'{xmul}:{ymul}'

    @property
    def fgcolor(self) -> int:
        """Return highres sprite color."""
        return self.color10


class VIC2:
    """VIC-II snapshot module."""

    def __init__(self, mod: VSFModule):
        self.mod = mod
        self.payload = mod.payload
        print('RAM base:', list(self.payload[1112:1112+4]))

    def __getattr__(self, name: str) -> int:
        reg = -1
        try:
            reg = int(name, 16) - 0xd000
        except ValueError:
            pass
        # if len(name) != 4 or not name.startswith('d'):
        if reg < 0x00 or reg >= 0x3f:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'.")
        return self.payload[1119 + reg]

    def color_ram(self) -> memoryview:
        """Return Color RAM."""
        return self.payload[43:43 + 1000]

    def getreg(self, num: int) -> int:
        """Return register value."""
        if num >= 0xd000:
            num -= 0xd000
        if num < 0 or num >= 0xff:      # FIXME TODO - max reg.
            raise ValueError(f'Invalid VIC-II register {num}')
        return self.payload[VIC_REG_OFFSET + num]

    def graphics_mode(self) -> GraphicsMode:
        """Return graphics mode."""
        ecm = (self.getreg(0xd011) & 0b0100_0000) >> 4
        bmm = (self.getreg(0xd011) & 0b0010_0000) >> 4
        mcm = (self.getreg(0xd016) & 0b0001_0000) >> 4
        num_mode = ecm | bmm | mcm
        return GraphicsMode(num_mode)

    def sprite(self, num: int) -> Sprite:
        """@@@"""
        if not 0 <= num <= 7:
            raise ValueError(f'Invalid sprite number {num}')
        status = (self.getreg(0xd015) & (1 << num)) != 0
        highx = 0x100 if (self.getreg(0xd010) & (1 << num)) != 0 else 0
        posx = highx + self.getreg(0xd000 + 2 * num + 0)
        posy = self.getreg(0xd000 + 2 * num + 1)
        multicolor = (self.getreg(0xd01c) & (1 << num)) != 0
        color01 = self.getreg(0xd025)
        color10 = self.getreg(0xd027 + num) & 0x0f
        color11 = self.getreg(0xd026)
        xexp = (self.getreg(0xd01d) & (1 << num)) != 0
        yexp = (self.getreg(0xd017) & (1 << num)) != 0
        return Sprite(num, status, posx, posy, multicolor, color01, color10, color11,
                      xexp=xexp, yexp=yexp)

    @property
    def d011(self) -> int:
        """Control Register 1 ($d011).

        %xxxxxx11 -> bank0: $0000-$3fff
        %xxxxxx11 -> bank1: $4000-$7fff
        %xxxxxx11 -> bank2: $8000-$bfff
        %xxxxxx11 -> bank3: $c000-$ffff
        """
        return self.getreg(0xd011)

    @property
    def d015(self) -> int:
        """Sprite Enable Register ($d015)."""
        return self.getreg(0xd015)

    @property
    def d016(self) -> int:
        """Control Register 2 ($d016)."""
        return self.getreg(0xd016)

    @property
    def d018(self) -> int:
        """Memory Control Register ($d018)."""
        return self.getreg(0xd018)

    @property
    def d020(self) -> int:
        """Border Color Register ($d020)."""
        return self.getreg(0xd020) & 0x0f

    @property
    def d021(self) -> int:
        """Background Color Register ($d021)."""
        return self.getreg(0xd021) & 0x0f

    @property
    def d025(self) -> int:
        """Sprite extra color 1 0b01 ($d025)."""
        return self.getreg(0xd025) & 0x0f

    @property
    def d026(self) -> int:
        """Sprite extra color 2 0b11 ($d026)."""
        return self.getreg(0xd026) & 0x0f

    @property
    def background_color(self) -> int:
        """Background color ($d021)."""
        return self.d021

    @property
    def border_color(self) -> int:
        """Border color ($d020)."""
        return self.d020

    @property
    def memory_setup_register(self) -> int:
        """Memory setup register ($d018)."""
        return self.d018

    def has_active_sprites(self) -> bool:
        """Return True if at least one sprite is active."""
        return self.d015 != 0x00

    def info(self, dd00: int) -> None:
        """@@@"""
        def reginfo(name: str, value: int, desc: str) -> None:
            """Print register info."""
            print(f'   ${name} = ${value:02x} (%{value:08b})  {desc}')

        print('VIC-II Registers:')
        reginfo('d011', self.d011, 'Screen Control Register 1')
        reginfo('d012', self.d012, 'Current Raster Line')
        # d013, d014 - light pen x and y coord.
        reginfo('d015', self.d015, 'Sprite Enable')
        reginfo('d016', self.d016, 'Screen Control Register 2')
        reginfo('d017', self.d017, 'Sprite Double Height')
        reginfo('d018', self.d018, 'Memory Setup Register')
        # d019 - Interrupt status.
        # d01a - Interrupt control.
        reginfo('d01b', self.d01b, 'Sprite Priority')
        reginfo('d01c', self.d01c, 'Sprite Color Mode')
        reginfo('d01d', self.d01d, 'Sprite Double Width')
        reginfo('d01e', self.d01e, 'Sprite-Sprite Collision')
        reginfo('d01f', self.d01f, 'Sprite-Background Collision')
        reginfo('d020', self.d020,
                f'Border Color -- {COLOR_NAME[self.d020 & 0x0f]}')
        reginfo('d021', self.d021,
                f'Background Color -- {COLOR_NAME[self.d021 & 0x0f]}')
        reginfo('d022', self.d022,
                f'Extra Background Color #1 -- {COLOR_NAME[self.d022 & 0x0f]}')
        reginfo('d023', self.d023,
                f'Extra Background Color #2 -- {COLOR_NAME[self.d023 & 0x0f]}')
        reginfo('d024', self.d024,
                f'Extra Background Color #3 -- {COLOR_NAME[self.d024 & 0x0f]}')
        reginfo('d025', self.d025,
                f'Sprite Extra Color #1 (%01) -- {COLOR_NAME[self.d025 & 0x0f]}')
        reginfo('d026', self.d026,
                f'Sprite Extra Color #2 (%11) -- {COLOR_NAME[self.d026 & 0x0f]}')

        vic_bank_addr = 0xc000 - 0x4000 * (dd00 & 0b0000_0011)

        print('Sprites:')
        # XXX print('   Multicolor %01 :', self.getreg(0xd025))
        # XXX print('   Multicolor %11 :', self.getreg(0xd026))
        for num in range(8):
            sprite = self.sprite(num)
            status = 'on' if sprite.status else 'off'
            multi = 'yes' if sprite.multicolor else 'no'
            if sprite.multicolor:
                colorstr = f'%01={sprite.color01:2} %10={sprite.color10:2} %11={sprite.color11:2}'
            else:
                colorstr = f'fg={sprite.fgcolor}'
            print((
                f'   Sprite {sprite.num} : {status:3}  ({sprite.posx:>3},{sprite.posy:>3})'
                f'  {sprite.exp}'
                f'  multi={multi:3}  {colorstr}'
            ))

        gfx_mode = self.graphics_mode()

        print('Graphics:')
        print('   Mode . . . . . . :', gfx_mode)
        print(f'   VIC bank address : ${vic_bank_addr:04x} ({vic_bank_addr})')
        if gfx_mode in (GraphicsMode.BITMAP, GraphicsMode.MULTICOLOR):
            bitmap_addr = vic_bank_addr + 8192 * ((self.d018 >> 3) & 1)
            screen_addr = vic_bank_addr + 1024 * (self.d018 >> 4)
            print(f'   Bitmap address . : ${bitmap_addr:04x} ({bitmap_addr})')
            print(f'   Screen address . : ${screen_addr:04x} ({screen_addr})')
        else:
            font_addr = vic_bank_addr + 2048 * ((self.d018 >> 1) & 0b111)
            screen_addr = vic_bank_addr + 1024 * (self.d018 >> 4)
            print(f'   Font address . . : ${font_addr:04x} ({font_addr})')
            print(f'   Screen address . : ${screen_addr:04x} ({screen_addr})')

            # https://www.c64-wiki.com/wiki/VIC_bank
            rom_font = font_addr in (0x1000, 0x1800, 0x9000, 0x9800)
            # rom_font = True
            # if vic_bank_addr in (0x4000, 0xc000):
            #    rom_font = False
            print('   ROM font . . . . :', rom_font)

            # 47c81fcda8e30feb67b7b3a04beaa5fa2baee126
            # 410b520d7938790602dce07bb9ce8ef4412dcff7
            # adc7c31e18c7c7413d54802ef2f4193da14711aa

            # XXX:
            # font_sum = new('sha1', self.mem.ram(font_addr, 4096)).hexdigest(); print(font_sum)
            # font_sum = new('sha1', self.mem.ram(font_addr, 2048)).hexdigest(); print(font_sum)
            # font_sum = new('sha1', self.mem.ram(font_addr + 2048, 2048)).hexdigest()
            # print(font_sum)
            # font_sum = blake2b(self.mem.ram(font_addr, 4096)).hexdigest(); print(font_sum)
            # font_sum = blake2s(self.mem.ram(font_addr, 4096)).hexdigest(); print(font_sum)

    def version(self) -> str:
        """Return module version."""
        return self.mod.version()

    def __str__(self) -> str:
        return ', '.join([
            f'{self.__class__.__name__}(start=0x{self.mod.start_pos:x}, size={self.mod.size:_}',
            f'ver={self.mod.version()})'
        ])


# vim: set sts=4 et sw=4:
