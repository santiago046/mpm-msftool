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
import shutil
import struct

from pathlib import Path


class InvalidMSFFileError(Exception):
    """Error when the signature does not match."""

    pass


class InvalidMSFVersionError(Exception):
    """Error when the version does mot match "2"."""

    pass


class NoMP3FilesFoundError(Exception):
    """Error when no MP3 files is found."""

    pass


class UnsafeFileNameError(Exception):
    """Error when file name is not ASCII safe."""

    pass


class MSFFile:
    """
    Represents an MSF (Max Payne Sound Files) that can pack a directory
    of MP3 files or unpack MP3 files to a directory

    Attributes:
        SIGNATURE: The expected signature for an MSF file.
        VERSION: The expected version of the MSF file format.

    Methods:
        pack(src_dir: Path, dst_file: Path): Pack a directory of MP3
            files into an MSF fils.
        unpack(dst_dir: Path, src_file: Path): Unpack the contents of
            an MSF file to a directory.
    """

    SIGNATURE = (0x00, 0x00, 0x03, 0xE7)
    VERSION = 2

    @classmethod
    def pack(cls, src_dir: Path, dst_file: Path):
        """
        Pack a directory of MP3 files into an MSF file.

        Args:
            src_dir: The path of the directory containing the MP3 files
                to pack.
            dst_file: The path of the MSF file to create.

        Raises:
            FileNotFoundError: If the source directory does not exist.
            OSError: If the source directory is not a directory or the
                destination file already exists.
            NoMP3FilesFoundError: If no MP3 files are found in the
                source directory.
            UnsafeFileNameError: If a file name in the source directory
                is not ASCII-safe.
        """

        # Check src_dir
        if not src_dir.exists():
            raise FileNotFoundError(f"'{src_dir}' does not exist")
        elif not src_dir.is_dir():
            raise OSError(f"'{src_dir}' is not a directory")

        # Check dst_file
        if dst_file.exists():
            raise OSError(f"'{dst_file}' already exists")
        else:
            try:
                dst_file.touch()
            except:
                raise OSError(f"'{dst_file}' cannot be created")

        # Create a list of MP3 files
        mp3_list = {
            file: {
                "relative_path": str(file.relative_to(src_dir)),
                "relative_path_length": len(str(file.relative_to(src_dir))),
                "size": file.stat().st_size,
            }
            for file in src_dir.rglob("*.[mM][pP]3")
        }

        # Check if the list is empty
        if not mp3_list:
            dst_file.unlink()
            raise NoMP3FilesFoundError(f"No MP3 files found in '{src_dir}'")

        # Check if there is any unsafe ASCII file name
        for mp3_file, info in mp3_list.items():
            if not info["relative_path"].isascii():
                dst_file.unlink()
                raise UnsafeFileNameError(f"'{mp3_file}' is unsafe ASCII name")

        # Calculate header size
        header_size = 12 + sum(
            info["relative_path_length"] + 9
            for mp3file, info in mp3_list.items()
        )

        with io.BytesIO() as header_buffer:
            # Generate header
            header_buffer.write(
                struct.pack(
                    ">4BII", *cls.SIGNATURE, cls.VERSION, len(mp3_list)
                )
            )

            mp3_data_offset = header_size
            for mp3_file, info in mp3_list.items():
                header_buffer.write(
                    struct.pack(
                        ">IIB",
                        mp3_data_offset,
                        info["size"],
                        info["relative_path_length"],
                    )
                )
                header_buffer.write(info["relative_path"].encode("ASCII"))

                mp3_data_offset += info["size"]

            # Write the MSF file
            with open(dst_file, "wb") as msf_file:
                msf_file.write(header_buffer.getvalue())

                # Concatenate MP3 files data
                for mp3_file in mp3_list:
                    with mp3_file.open("rb") as data:
                        shutil.copyfileobj(data, msf_file)

    @classmethod
    def unpack(cls, dst_dir: Path, src_file: Path):
        """
        Unpack the contents of an MSF file to a directory.

        Args:
            dst_dir (Path): Path object to the directory where the files
                will be saved.
            src_file (Path): Path object to the MSF file to unpack.


        Raises:
            FileNotFoundError: If the source file does not exist or is a
                directory.
            InvalidMSFFileError: If the source file is not a valid MSF
                file.
            InvalidMSFVersionError: If the MSF file version does not
                match the expected version.
        """

        # Check src_file
        if not src_file.exists():
            raise FileNotFoundError(f"'{src_file}' does not exist")
        elif src_file.is_dir():
            raise FileNotFoundError(
                f"'{src_file}' is a directory, expected a file"
            )

        dst_dir.mkdir(parents=True, exist_ok=True)

        with src_file.open("rb") as msf_file:
            # Check signature and version match
            if struct.unpack(">4B", msf_file.read(4)) != cls.SIGNATURE:
                raise InvalidMSFFileError(f"'{src_file}' is not a MSF file")
            elif struct.unpack(">I", msf_file.read(4))[0] != cls.VERSION:
                raise InvalidMSFVersionError(
                    f"version of '{msf_file}' does not match '2'"
                )

            # Read total of files
            total_of_files = struct.unpack(">I", msf_file.read(4))[0]
            print(f"Total of files: {total_of_files}")

            # Loop through each file
            for _ in range(total_of_files):
                file_offset, file_size, file_name_length = struct.unpack(
                    ">IIB", msf_file.read(9)
                )
                file_name = msf_file.read(file_name_length).decode("ASCII")

                current_position = msf_file.tell()

                # Seek to file content location
                msf_file.seek(file_offset)

                # Create subdirectories
                output_file_name = dst_dir / file_name
                output_file_name.parent.mkdir(parents=True, exist_ok=True)

                # Write output file
                with output_file_name.open("wb") as output_file:
                    output_file.write(msf_file.read(file_size))

                # Seek back to table of file information
                msf_file.seek(current_position)
