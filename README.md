# xsnap

**xsnap** allows you to extract screenshots from various (in the future)
emulator snapshots files.

## Supported

- VICE C64 snapshot files (new and old formats)
    - Hires bitmap screens
    - Multicolor bitmap screens
    - Standard character screens

## Output formats

C64 hires bitmap screens:

- aas - Art Studio Hires
- doo - Doodle!
- hpc - HiPic Creator

C64 multicolor bitmap screens:
- a64 - Artist 64
- ami - Amica Paint
- art - Advanced Art Studio (OCP Art Studio)
- che - Cheese Paint
- drp - Draz Paint (compressed)
- drz - Draz Paint (uncompressed)
- gas - Graphic Assault System
- koa - Koala Painter
- vid - Vidcom 64
- zom - Zoomatic

C64 standard character screens:

- pdr (Petdraw 64)
- pet (PETSCII Editor 4)

## Requirements

- Python 3.9 or higher
- make (gmake on BSD)

## Installation

You can install **xsnap** from [Github][repo].

```sh
git clone https://github.com/amnr/xsnap/
cd xsnap
make binary
# Copy xsnap anywhere you like.
# Rename xsnap to xsnap.pyz when on Windows.
```

## Usage

```sh
$ xsnap snapshot.vsf        # Running „make binary” required.
```

```sh
$ ./run.sh snapshot.vsf     # Testing only.
```

## Sample Usage

### Hires bitmap screen

```
$ xsnap './Treasure Island Dizzy.vsf'
VSF Snapshot version 2.0, machine C64, VICE version 3.7.1.0 rev. 0
[…]
Graphics:
   Mode . . . . . . : hires bitmap
   VIC bank address : $4000 (16384)
   Bitmap address . : $6000 (24576)
   Screen address . : $5c00 (23552)
Writing hires screen images:
  Treasure Island Dizzy.hpc :  9003 bytes
  Treasure Island Dizzy.aas :  9009 bytes
  Treasure Island Dizzy.doo :  9218 bytes
$ _
```

VICE emulator screenshot:

![Dizzy Snapshot](https://amnr.github.io/xsnap/Treasure%20Island%20Dizzy.x64.png)

Output image:

![Dizzy Image](https://amnr.github.io/xsnap/Treasure%20Island%20Dizzy.hpc.png)

### Multicolor bitmap screen

```
$ ./xsnap Draconus.vsf
VSF Snapshot version 2.0, machine C64, VICE version 3.7.1.0 rev. 0
[…]
Graphics:
   Mode . . . . . . : multicolor bitmap
   VIC bank address : $c000 (49152)
   Bitmap address . : $e000 (57344)
   Screen address . : $d000 (53248)
Writing multicolor screen images:
  Draconus.zom :  7039 bytes
  Draconus.ami :  7046 bytes
  Draconus.drp :  7057 bytes
  Draconus.koa : 10003 bytes
  Draconus.drz : 10051 bytes
  Draconus.gas : 10342 bytes
$_
```

VICE emulator screenshot:

![Draconus Snapshot](https://amnr.github.io/xsnap/Draconus.x64.png)

Output image:

![Draconus Image](https://amnr.github.io/xsnap/Draconus.koa.png)

### Standard character screen

```
VSF Snapshot version 2.0, machine C64, VICE version 3.7.1.0 rev. 0
[…]
Graphics:
   Mode . . . . . . : standard character
   VIC bank address : $0000 (0)
   Font address . . : $2800 (10240)
   Screen address . : $0400 (1024)
   ROM font . . . . : False
Writing standard character screen images:
  Gary.pet :  2026 bytes
  Gary.pdr :  2029 bytes
$_
```

VICE emulator screenshot:

![Gary Snapshot](https://amnr.github.io/xsnap/Gary.x64.png)

Output image:

![Gary Image](https://amnr.github.io/xsnap/Gary.pdr.png)

[repo]: https://github.com/amnr/snap64/

<!-- vim: set sts=4 et sw=4: -->
