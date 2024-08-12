"""Main."""

import sys

_MINVER = (3, 9)

if sys.version_info < _MINVER:
    print('Error: required python 3.9 (or later), found python',
          f'{sys.version_info.major}.{sys.version_info.minor}')
    raise SystemExit(1)

try:
    from .xsnap.main import main
    main()
except ImportError:
    # Note: mypy is still silly enough.
    from xsnap.main import main      # type: ignore[import-not-found,no-redef]
    main()

# vim: set sts=4 et sw=4:
