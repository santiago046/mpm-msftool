from setuptools import setup, find_packages

setup(
    name="mpm-msftool",
    version="1.0.0",
    description="CLI tool to unpack/pack MSF files from Max Payne Mobile",
    author="santiago046",
    license="GPLv3",
    url="https://github.com/santiago046/mpm-msftool",
    packages=find_packages(),
    entry_points={"console_scripts": ["msftool = msftool.__main__:main"]},
)
