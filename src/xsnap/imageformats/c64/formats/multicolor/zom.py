# pylint: disable=duplicate-code
"""Zoomatic."""

from .. import rle
from ...scrtypes import MultiColorScreen

LDADDR = b'\x00\x60'

BUFSIZE = 10_001

MAX_REPEAT = 256


def packbuf(buf: bytes, esc: int, verbose: bool = False) -> bytes:
    """Pack data."""
    assert len(buf) == BUFSIZE

    result = [LDADDR]

    for val, count in rle.rleiter(buf, MAX_REPEAT):
        if verbose:
            print(f'{count:3} x ${val:02x} ->', end=' ')
        if count > 1:
            # RLE run of any byte.
            if count == 256:
                count = 0
            if verbose:
                print(f'${esc:02x} ${count:02x} ${val:02x}')
            # Note: reversed order.
            result.append(bytes([val, count, esc]))
        elif val != esc:
            # Single non-escape value.
            if verbose:
                print(f'${val:02x}')
            result.append(bytes([val]))
        else:
            # Single escape $c2 value.
            if verbose:
                print(f'${esc:02x} $01 ${val:02x}')
            # Note: reversed order.
            result.append(bytes([val, 0x01, esc]))

    # Escape byte.
    result.append(bytes([esc]))

    return b''.join(result)


def pack(image: MultiColorScreen, escval: int = -1,
         verbose: bool = False) -> bytes:
    """Zoomatic."""
    assert escval <= 0xff

    last_byte = int.to_bytes((ord(image.border) << 4) | ord(image.bgcolor))

    data = b''.join([
        image.bitmap,
        image.screen,
        image.colors,
        last_byte
    ])

    esc = escval
    if escval < 0:
        esc = rle.find_esc_byte(data)

    return packbuf(data, esc, verbose=verbose)

# vim: set sts=4 et sw=4:
