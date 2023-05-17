from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="msffile",
    version="2.0.0",
    description="Unpacker/packer for MSF files from Max Payne Mobile",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="santiago046",
    license="GPLv3",
    url="https://github.com/santiago046/mpm-msftool",
    packages=find_packages(),
    entry_points={"console_scripts": ["msftool = msffile.__main__:main"]},
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Games/Entertainment",
    ],
    project_urls={"Source Code": "https://github.com/santiago046/mpm-msftool"},
)
