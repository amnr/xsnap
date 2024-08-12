"""VSF Modules."""

from enum import Enum
from io import BufferedReader
from pathlib import Path
from struct import unpack

from .generic import VSFError, VSFModule

from .c64mem import C64Mem
from .cia2 import CIA2
from .vic2 import VIC2


__all__ = ['ViceSnapshotFile', 'VSFError']


VSF_MAGIC = b'VICE Snapshot File\x1a'
VICE_VERSION_MAGIC = b'VICE Version\x1a'


class Machine(Enum):
    """Machine."""
    C64 = b'C64'
    C64DTV = b'C64DTV'
    C128 = b'C128'
    PLUS4 = b'PLUS4'
    PET = b'PET'
    SCPU64 = b'SCPU64'
    VIC20 = b'VIC20'
    CBM2 = b'CBM-II'
    CBM5 = b'CBM-II-5x0'


class Module(Enum):
    """Module."""
    C64MEM = b'C64MEM'
    CIA2 = b'CIA2'
    VIC2 = b'VIC-II'


class ViceSnapshotFile:     # pylint: disable=too-many-instance-attributes
    """VICE Snapshot."""

    def __init__(self, fobj: BufferedReader):
        self.fobj = fobj
        fobj.seek(0)

        self.magic = fobj.read(len(VSF_MAGIC))
        if self.magic != VSF_MAGIC:
            raise VSFError('file is not a VSF snapshot - invalid magic')

        self.major, self.minor, self.machine = unpack('<BB16s', fobj.read(18))
        if len(self.machine) != 16:
            raise VSFError('unexpected end of file')
        self.machine = self.machine.rstrip(b'\x00')

        version_magic = fobj.read(len(VICE_VERSION_MAGIC))
        if version_magic == VICE_VERSION_MAGIC:
            self.vice_version = unpack('<4B', fobj.read(4))
            self.vice_revision = unpack('<L', fobj.read(4))[0]
        else:
            print('Pre VICE 2.4.30 snapshot')
            fobj.seek(-len(VICE_VERSION_MAGIC), 1)
            self.vice_version = (0, 0, 0, 0)
            self.vice_revision = 0

        machine = self.machine.decode()
        print(f'VSF Snapshot version {self.version()}, machine {machine}', end='')
        if self.major > 1:
            print(', VICE version', '.'.join(str(_) for _ in self.vice_version),
                  'rev.', self.vice_revision, end='')
        print()

        # Read all modules.
        self.modules = []
        try:
            while True:
                # Check for EOF.
                pos = fobj.tell()
                if fobj.read(1) == b'':
                    break
                fobj.seek(pos)

                # Read next module.
                mod = VSFModule.from_file(fobj)
                self.modules.append(mod)
        except EOFError:
            pass        # XXX: fix it.

    def basename(self) -> str:
        """Return base file name (without an extension)."""
        loname = self.fobj.name.lower()
        name = self.fobj.name
        # XXX: dirty hack.
        if loname.endswith('.bz2') or loname.endswith('.gz'):
            name = name.partition('.')[0]
        return Path(name).stem

    def dirname(self) -> Path:
        """Return the file directory."""
        return self.fobj.dirname

    def is_c64(self) -> bool:
        """Return True is this is a C64 snapshot file."""
        return self.machine == Machine.C64.value

    def version(self) -> str:
        """Version number."""
        return f'{self.major}.{self.minor}'

    def cia2(self) -> CIA2:
        """CIA2."""
        for mod in self.modules:
            if mod.magic == Module.CIA2.value:
                return CIA2(mod)
        raise KeyError('CIA2 module not found')

    def c64mem(self) -> C64Mem:
        """C64 memory."""
        for mod in self.modules:
            if mod.magic == Module.C64MEM.value:
                return C64Mem(mod)
        raise KeyError('C64MEM module not found')

    def vic2(self) -> VIC2:
        """VIC2."""
        for mod in self.modules:
            if mod.magic == Module.VIC2.value:
                return VIC2(mod)
        raise KeyError('VIC2 module not found')

# vim: set sts=4 et sw=4:
