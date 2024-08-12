"""@@@"""

import random
from typing import Iterator


def find_esc_byte(buf: bytes) -> int:
    """Find the least common value in a buffer."""
    counts = [0] * 256
    for val in buf:
        counts[val] += 1
    return counts.index(min(counts))


def random_buffer(size: int) -> bytes:
    """Generate buffer of random data."""
    return random.randbytes(size)


def rleiter(buf: bytes, max_repeat: int) -> Iterator[tuple[int, int]]:
    """Iterate data and return (value, count) pairs."""
    assert max_repeat <= 256
    count = 0
    prev = None
    for val in buf:
        if val == prev:
            if count == max_repeat:
                assert prev is not None     # Shut mypy up.
                yield (prev, count)
                count = 1
            else:
                count += 1
        else:
            if prev is not None:
                yield (prev, count)
            count = 1
            prev = val

    assert prev is not None     # Shut mypy up.
    yield (prev, count)

# vim: set sts=4 et sw=4:
