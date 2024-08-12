#!/usr/bin/env python3
"""VSNAP."""

import argparse
from pathlib import Path

from . import vice
from .utils import fileutils, logutils as log


USAGE_EPILOG = '''
xsnap home page: <https://github.com/amnr/xsnap/>
'''


def parse_args() -> argparse.Namespace:
    """Parse args."""
    parser = argparse.ArgumentParser(
        epilog=USAGE_EPILOG,
        formatter_class=lambda prog: argparse.RawDescriptionHelpFormatter(
            prog, max_help_position=30, width=100))
    # parser.add_argument('-f', '--overwrite', action='store_true')
    # parser.add_argument('-i', '--info', action='store_true')
    parser.add_argument('-o', '--outdir', type=Path, help='output directory')
    parser.add_argument('snapshot_file', type=Path, nargs='+', help='VSF snapshot file')
    args = parser.parse_args()

    # Outdir must be a directory.
    if isinstance(args.outdir, Path) and not args.outdir.is_dir():
        parser.error(f"not a directory: '{args.outdir}'")

    return args


def extract_images(file: Path, outdir: Path, showinfo: bool = False) -> None:
    """Extract images from snapshot file."""
    with fileutils.open_file(file) as fobj:
        if vice.is_vice_snapshot(fobj):
            vice.extract_vice(fobj, outdir, showinfo=showinfo)
        else:
            print(f"File '{file}' - file format not recognized")


def process_files() -> None:
    """Process snapshot files."""
    args = parse_args()

    for file in args.snapshot_file:
        try:
            extract_images(file, args.outdir)   # XXX: args.info)
        except (FileNotFoundError, IsADirectoryError, PermissionError) as err:
            log.error(err)


def main() -> None:
    """Main."""
    try:
        process_files()
    except (BrokenPipeError, KeyboardInterrupt):
        raise SystemExit(1)     # pylint: disable=raise-missing-from


if __name__ == '__main__':
    main()

# vim: set sts=4 et sw=4:
