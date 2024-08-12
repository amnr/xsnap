# pylint: disable=duplicate-code
"""Graphic Assault System image."""

from .. import rle
from ...scrtypes import MultiColorScreen

LDADDR = b'\x00\x60'

MAGIC = 0xa0

BUFSIZE = 10_001

REPEAT = 255

FOOTER = "gas UTILITY COMPRESSED GRAPHIC- bRUCE bOWDEN hEURISTICS 1987,1988".encode()


def packbuf(buf: bytes, verbose: bool = False) -> bytes:
    """Pack data."""
    assert len(buf) == BUFSIZE

    result = [
        LDADDR,
        int.to_bytes(MAGIC)
    ]

    for val, count in rle.rleiter(buf, REPEAT):
        if verbose:
            print(f'{count:3} x ${val:02x} ->', end=' ')
        # RLE run.
        if verbose:
            print(f'${count:02x} ${val:02x}')
        result.append(bytes([count, val]))

    # EOF marker.
    result.append(b'\x00\x00')

    result.append(FOOTER)

    return b''.join(result)


def pack(image: MultiColorScreen, verbose: bool = False) -> bytes:
    """Graphic Assault System image."""
    data = b''.join([
        image.bitmap,
        image.screen,
        image.colors,
        image.bgcolor
    ])

    assert len(data) == BUFSIZE

    return packbuf(data, verbose=verbose)

# vim: set sts=4 et sw=4:
