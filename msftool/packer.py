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


import io
import mmap
import struct


def pack_files(src_dir, dest_file):
    file_list = [file for file in src_dir.rglob("*.[mM][pP]3")]

    if not file_list:
        print("No MP3 files found!")
        return 1
    # Calculate the header size
    header_size = 12 + sum(
        [len(str(file.relative_to(src_dir))) + 9 for file in file_list]
    )

    with io.BytesIO() as header_buf, io.BytesIO() as data_buf, open(
        dest_file, "wb"
    ) as msf_file:
        signature = (0x00, 0x00, 0x03, 0xE7, 0x00, 0x00, 0x00, 0x02)
        header_buf.write(struct.pack(">8BI", *signature, len(file_list)))

        file_offset = header_size
        for file in sorted(file_list):
            file_relative = str(file.relative_to(src_dir))
            header_buf.write(
                struct.pack(
                    ">IIB",
                    file_offset,
                    file.stat().st_size,
                    len(file_relative),
                )
            )
            header_buf.write(file_relative.encode("ASCII"))
            file_offset += file.stat().st_size

            data_buf.write(file.read_bytes())

        msf_file.write(header_buf.getvalue())
        msf_file.write(data_buf.getvalue())
