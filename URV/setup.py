"""Package description."""
import sys

import setuptools


if sys.platform != 'win32':
    print('This package supports only Windows.')
    exit(1)

if sys.version_info < (3, 6):
    print('This package requires Python version 3.6 and higher.')
    exit(1)

with open("requirements.txt", "r") as f:
    install_requires = f.readlines()

setuptools.setup(
    name="urv_automation",
    version="0.0.1",
    author="Marek Bohdan",
    author_email="mongoose@soeidental.com",
    description="URV test automation solution",
    long_description="Test automation solution for SOE Reporting Views",
    url="https://henryscheinone.co.nz/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Windows",
    ],
    python_requires='>=3.6',
    install_requires=install_requires,
)
