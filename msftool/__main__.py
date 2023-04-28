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


from .cli import parse_arguments
from .packer import pack_files
from .unpacker import unpack_files


def main():
    arguments = parse_arguments()

    if arguments.mode == "pack":
        pack_files(arguments.path, arguments.output)
    if arguments.mode == "unpack":
        unpack_files(arguments.output, arguments.path)


if __name__ == "__main__":
    main()
