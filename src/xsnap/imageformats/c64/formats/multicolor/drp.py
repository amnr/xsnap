# pylint: disable=duplicate-code
"""Draz Paint (compressed)."""

from .. import rle
from ...scrtypes import MultiColorScreen

LDADDR = b'\x00\x58'

MAGIC = "DRAZPAINT 2.0".encode()

BUFSIZE = 10_049

MAX_REPEAT = 255


def packbuf(buf: bytes, esc: int, verbose: bool = False) -> bytes:
    """Pack data."""
    assert len(buf) == BUFSIZE

    result = [
        LDADDR,
        MAGIC,
        int.to_bytes(esc)
    ]

    for val, count in rle.rleiter(buf, MAX_REPEAT):
        if verbose:
            print(f'{count:3} x ${val:02x} ->', end=' ')
        if count > 1:
            # RLE run of any byte.
            if verbose:
                print(f'${esc:02x} ${count:02x} ${val:02x}')
            result.append(bytes([esc, count, val]))
        elif val != esc:
            # Single non-escape value.
            if verbose:
                print(f'${val:02x}')
            result.append(bytes([val]))
        else:
            # Single escape $c2 value.
            if verbose:
                print(f'${esc:02x} $01 ${val:02x}')
            result.append(bytes([esc, 0x01, val]))

    return b''.join(result)


def pack(image: MultiColorScreen, escval: int = -1,
         verbose: bool = False) -> bytes:
    """Draz Paint (compressed)."""
    assert escval <= 0xff

    data = b''.join([
        image.colors,
        bytes(24),
        image.screen,
        bytes(24),
        image.bitmap,
        image.bgcolor
    ])

    assert len(data) == BUFSIZE

    esc = escval
    if escval < 0:
        esc = rle.find_esc_byte(data)

    return packbuf(data, esc, verbose=verbose)

# vim: set sts=4 et sw=4:
