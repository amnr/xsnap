#!/usr/bin/env python3
"""File utils."""

import bz2
import gzip
import lzma
from datetime import datetime
from io import BufferedReader
from pathlib import Path


def open_file(path: Path) -> BufferedReader:
    """Open the file."""
    # Gzip file.
    try:
        fobj = gzip.open(path)
        fobj.read(1)
        fobj.seek(0)
        return fobj
    except gzip.BadGzipFile:
        pass

    # Bzip2 file.
    try:
        fobj = bz2.open(path)
        fobj.read(1)
        fobj.seek(0)
        fobj.name = path.name           # XXX: dirty hack.
        fobj.dirname = path.parent      # XXX: dirty hack.
        return fobj
    except OSError:
        pass

    # LZMA file.
    try:
        fobj = lzma.open(path)
        fobj.read(1)
        fobj.seek(0)
        fobj.name = path.name   # XXX: dirty hack.
        fobj.dirname = path.parent      # XXX: dirty hack.
        return fobj
    except lzma.LZMAError:
        pass

    # Uncompressed file.
    fobj = open(path, 'rb')         # pylint: disable=consider-using-with
    fobj.dirname = path.parent      # XXX: dirty hack.

    return fobj


def save_file(outdir: Path, name_stem: str, ext: str, data: bytes,
              overwrite: bool = False) -> bool:
    """Write file."""
    if not ext.startswith('.'):
        ext = '.' + ext

    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')

    filename = f'{name_stem}_{timestamp}{ext}'

    outfile = outdir / filename

    print('Writing', outfile, '...')

    if outfile.exists() and not overwrite:
        print('A file with that name already exists')
        return False

    outfile.write_bytes(data)

    return True


# vim: set sts=4 et sw=4:
