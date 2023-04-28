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


import struct


def unpack_files(dest_dir, msf_file):
    # Checking destination directory
    if dest_dir.exists() and not dest_dir.is_dir():
        print(f"'{dest_dir}' is not a directory, exiting")
        sys.exit(1)
    elif not dest_dir.exists():
        try:
            dest_dir.mkdir(parents=True)
        except OSError as e:
            print(e)
            print(f"Could not create '{dest_dir}' directory, exiting")
            sys.exit(1)

    with open(msf_file, "rb") as file:
        signature = file.read(8)

        # Check if file signature matches
        if signature != b"\x00\x00\x03\xe7\x00\x00\x00\x02":
            print("File signature does not match, exiting")
            sys.exit(1)

        total_of_files = struct.unpack(">I", file.read(4))[0]
        print(f"Total of files: {total_of_files}")

        # Reading table of file information
        for i in range(total_of_files):
            file_offset, file_size, file_name_length = struct.unpack(
                ">IIB", file.read(9)
            )
            file_name = file.read(file_name_length).decode("ASCII")

            current_position = file.tell()

            # Seeking to file content location
            file.seek(file_offset)

            output_file_name = dest_dir / file_name
            # Creating subdirectories
            output_file_name.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file_name, "wb") as output_file:
                output_file.write(file.read(file_size))

            # Seeking back to table of file information to read the next file
            file.seek(current_position)
