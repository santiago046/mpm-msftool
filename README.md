## mpm-msftool
A tool to unpack/pack .MSF files from Max Payne Mobile.

## Description
mpm-msftool is a command-line tool that allows you to extract and create .MSF files for Max Payne Mobile. A MSF (probably Max Payne Sound Files) is a package file that contains the sound resources (in MP3) of Max Payne Mobile.

With mpm-msftool, you can easily access and modify the sound files of the game, such as music, dialogues, effects, etc.

## Contents
- [Installation](#installation)
- [Usage](#usage)
  * [pack](#pack)
  * [unpack](#unpack)
- [Examples](#examples)
- [About MSF file](#about-msf-file)

## Installation
You can install mpm-msftool using pip:  
`pip install mpm-msftool`

After installing it, type `msftool -h` to see if it is working.

## Usage
### pack
```
usage: msftool pack [-h] [-o <file>] path

positional arguments:
  path                  path to the directory to pack

options:
  -h, --help            show this help message and exit
  -o <file>, --output <file>
                        output file name (default: MaxPayneSoundsv2.msf)
```

### unpack
```
usage: msftool unpack [-h] [-o <dir>] path

positional arguments:
  path                  path to the .MSF file to unpack

options:
  -h, --help            show this help message and exit
  -o <dir>, --output <dir>
                        output directory (default: mpm_sounds)
```

## Examples
Unpacking MaxPayneSoundsv2.msf to ~/mpm/MaxPayneSoundsv2/:  
`msftool unpack -o ~/mpm/MaxPayneSoundsv2 MaxPayneSoundsv2.msf`  

Packing ~/mpm/MaxPayneSoundsv2 to ~/mpm/MaxPayneSoundsv2.msf:  
`msftool pack -o ~/mpm/MaxPayneSoundsv2.msf ~/mpm/MaxPayneSoundsv2`

## About MSF file
A .MSF is a package file that can be found in the game's OBB.

The MSF file format is very simple:

| OFFSET |       FIELD      |  TYPE  |
| :----: | :--------------: | :----: |
|  0x00  | Magic number     | uint64 |
|  0x08  | Total of files   | uint32 |
|        |                  |        |
|  0x0C¹ | File offset²     | uint32 |
|  0x10  | File size        | uint32 |
|  0x14  | File name length | uint8  |
|  0x15  | File path name   | ASCII³ |

1 - start of files table infomation;  
2 - it should to point at the end of files info table/start of files data;  
3 - size defined by the previous entry.
