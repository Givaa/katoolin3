from setuptools import setup, find_packages

setup(
    name="katoolin3",
    version="3.1.0",
    description="Install Kali Linux tools on Debian/Ubuntu",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="LionSec (original), katoolin3 contributors",
    license="GPLv2",
    packages=find_packages(),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "katoolin3=katoolin3.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Environment :: Console",
        "Topic :: Security",
    ],
)
