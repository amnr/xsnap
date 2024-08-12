"""Generic VSF Module."""

from dataclasses import dataclass
from io import BufferedReader
from struct import unpack


class VSFError(Exception):
    """VSF Error."""


@dataclass
class VSFModule:
    """VSF Module."""

    HEADER_SIZE = 22

    start_pos: int
    magic: bytes
    major: int
    minor: int
    size: int
    payload: memoryview

    @staticmethod
    def from_file(fobj: BufferedReader) -> 'VSFModule':
        """Create module from file."""
        start_pos = fobj.tell()
        magic, major, minor, mod_size = unpack('<16sBBL', fobj.read(VSFModule.HEADER_SIZE))
        if mod_size < VSFModule.HEADER_SIZE:
            raise VSFError('unexpected end of file')
        magic = magic.rstrip(b'\x00')
        # bytes_left = start_pos + self.mod_size - fobj.tell()
        payload = memoryview(fobj.read(mod_size - VSFModule.HEADER_SIZE))
        return VSFModule(start_pos, magic, major, minor, mod_size, payload)

    def info(self) -> None:
        """Print module info."""
        magic = self.magic.rstrip(b'\x00').decode()
        print((
            f'  \033[96m{self.start_pos:07x}  \033[92m{magic:16}\033[0m'
            f'  {self.major}.{self.minor}  {self.size:>8}  {len(self.payload):>8}'
        ))

    def version(self) -> str:
        """Module version."""
        return f'{self.major}.{self.minor}'

    def __str__(self) -> str:
        magic = self.magic.rstrip(b'\x00').decode()
        return ((
            f'Module(start_pos={self.start_pos}, magic={magic}, major={self.major},'
            f' minor={self.minor}, size={self.size}, payload_size={len(self.payload)})'
        ))


# vim: set sts=4 et sw=4:
