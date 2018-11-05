# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name="metys",
    version="0.1.0",
    description="Multi-kernel/Multi-session Jupyter scientific report generator and literate programming tool.",
    license="MIT",
    author="Tarn W. Burton",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': ['metys=metys.__main__:main'],
    },
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ]
)
