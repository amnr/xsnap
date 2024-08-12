# pylint: disable=duplicate-code
"""Amica Paint."""

from .. import rle
from ...scrtypes import MultiColorScreen

LDADDR = b'\x00\x40'

BUFSIZE = 10_001

ESC = 0xc2

MAX_REPEAT = 255


def packbuf(buf: bytes, verbose: bool = False) -> bytes:
    """Pack data."""
    assert len(buf) == BUFSIZE

    result = [LDADDR]

    for val, count in rle.rleiter(buf, MAX_REPEAT):
        if verbose:
            print(f'{count:3} x ${val:02x} ->', end=' ')
        if count > 1:
            # RLE run of any byte.
            if verbose:
                print(f'$c2 ${count:02x} ${val:02x}')
            result.append(bytes([ESC, count, val]))
        elif val != ESC:
            # Single non-escape value.
            if verbose:
                print(f'${val:02x}')
            result.append(bytes([val]))
        else:
            # Single escape $c2 value.
            if verbose:
                print(f'${ESC:02x} $01 ${val:02x}')
            result.append(bytes([ESC, 0x01, val]))

    # EOF marker.
    result.append(b'\xc2\x00')

    return b''.join(result)


def pack(image: MultiColorScreen, verbose: bool = False) -> bytes:
    """Amica Paint."""
    data = b''.join([
        image.bitmap,
        image.screen,
        image.colors,
        image.bgcolor
    ])

    assert len(data) == BUFSIZE

    return packbuf(data, verbose=verbose)

# vim: set sts=4 et sw=4:
