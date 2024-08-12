#!/usr/bin/env python3
"""VSF (VICE Snapshot File).
"""

import tempfile
from io import BufferedReader
from pathlib import Path
from typing import Optional

from . import vsf
from .x64 import X64
from .. import imageformats
from ..utils import log


def is_vice_snapshot(fobj: BufferedReader) -> bool:
    """Return True if file is a VICE snapshot (VSF) file."""
    fobj.seek(0)
    return fobj.read(len(vsf.VSF_MAGIC)) == vsf.VSF_MAGIC


def export_hires_images(img: imageformats.c64.HiresImage, basename: str,
                        outdir: Path) -> None:
    """Export hires images."""
    formats = sorted([
        ('aas', img.as_aas()),
        ('doo', img.as_doo()),
        ('hpc', img.as_hpc())
    ], key=lambda _: len(_[1]), reverse=False)

    print('Writing hires screen images:')
    for ext, data in formats:
        fullpath = outdir / f'{basename}.{ext}'
        print(f'  {fullpath} : {len(data):5} bytes')
        fullpath.write_bytes(data)


def export_multi_images(img: imageformats.c64.MultiColorImage, basename: str,
                        outdir: Path) -> None:
    """Export multicolor images."""
    formats = sorted([
        ('ami', img.as_amica()),
        ('drp', img.as_drp()),
        ('drz', img.as_drz()),
        ('gas', img.as_graphic_assault_system()),
        ('koa', img.as_koala()),
        ('zom', img.as_zoomatic())
    ], key=lambda _: len(_[1]), reverse=False)

    print('Writing multicolor screen images:')
    for ext, data in formats:
        fullpath = outdir / f'{basename}.{ext}'
        print(f'  {fullpath} : {len(data):5} bytes')
        fullpath.write_bytes(data)


def export_text_images(img: imageformats.c64.TextImage, basename: str,
                       outdir: Path) -> None:
    """Export text images."""
    formats = sorted([
        ('pdr', img.as_pdr()),
        ('pet', img.as_pet())
    ], key=lambda _: len(_[1]), reverse=False)

    print('Writing standard character screen images:')
    for ext, data in formats:
        fullpath = outdir / f'{basename}.{ext}'
        print(f'  {fullpath} : {len(data):5} bytes')
        fullpath.write_bytes(data)


def extract_c64(snap: vsf.ViceSnapshotFile, outdir: Path) -> None:
    """Extract images from C64 snapshot file."""
    x64 = X64(snap)
    x64.show_info()

    if x64.has_active_sprites():
        log.warn((
            'snapshot file has active sprites,'
            ' screenshot images may not reflect the actual screen'
        ))

    bitmap = x64.bitmap_ram()
    colors = x64.color_ram()
    screen = x64.screen_ram()
    bgcolr = x64.background_color()
    border = x64.border_color()

    if x64.is_screen_multicolor():
        mimg = imageformats.c64.MultiColorImage(bitmap, screen, colors, bgcolr,
                                                border)
        export_multi_images(mimg, snap.basename(), outdir)
    elif x64.is_screen_hires():
        himg = imageformats.c64.HiresImage(bitmap, screen, border)
        export_hires_images(himg, snap.basename(), outdir)
    elif x64.is_screen_text():
        timg = imageformats.c64.TextImage(screen, colors, bgcolr, border,
                                          x64.memory_setup_register())
        export_text_images(timg, snap.basename(), outdir)
    else:
        log.error('Screen mode not yet supported')  # XXX: add mode name to error.


def extract_vice(fobj: BufferedReader, outdir: Optional[Path] = None,
                 showinfo: bool = False) -> bool:
    """@@@"""
    # Read snapshot file.
    try:
        snap = vsf.ViceSnapshotFile(fobj)
    except vsf.VSFError as err:
        log.error(err)
        return False

    if outdir is None:
        outdir = fobj.dirname

    if snap.is_c64():
        extract_c64(snap, outdir)
    else:
        print('VICE Snapshot,', snap.machine.decode(),
              'machine, screenshots unsupported')
        return False

    raise SystemExit

# vim: set sts=4 et sw=4:
