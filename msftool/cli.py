# mpm-msftool - A tool to unpack/pack .MSF files from Max Payne Mobile.
# Copyright (C) 2023 santiago046

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import argparse
import pathlib


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="A tool to unpack/pack Max Payne Mobile's MSF files",
        prog="msftool",
    )
    subparsers = parser.add_subparsers(
        dest="mode", help="tool mode", required=True
    )

    # Packing subparser arguments
    parser_pack = subparsers.add_parser(
        "pack",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help="pack a directory with .MP3 files to .MSF",
    )
    parser_pack.add_argument(
        "-o",
        "--output",
        default="MaxPayneSoundsv2.msf",
        help="output file name",
        metavar="<file>",
    )
    parser_pack.add_argument(
        "path", help="path to the directory to pack", type=pathlib.Path
    )

    # Unpacking subparser arguments
    parser_unpack = subparsers.add_parser(
        "unpack",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        help="unpack a .MSF file to a directory",
    )
    parser_unpack.add_argument(
        "-o",
        "--output",
        default="mpm_sounds",
        help="output directory",
        metavar="<dir>",
        type=pathlib.Path,
    )
    parser_unpack.add_argument("path", help="path to the .MSF file to unpack")

    return parser.parse_args()
