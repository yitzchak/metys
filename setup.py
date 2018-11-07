# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

exec(open("./metys/_version.py").read())

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name="metys",
    version=__version__,
    description="Multi-kernel/Multi-session Jupyter scientific report generator and literate programming tool.",
    license="MIT",
    author="Tarn W. Burton",
    packages=find_packages(),
    install_requires=[
        "jupyter_client"
    ],
    entry_points={
        'console_scripts': ['metys=metys.__main__:main'],
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
        'Topic :: Text Processing :: Markup',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python"
    ]
)
