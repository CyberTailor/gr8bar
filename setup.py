#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="gr8bar",
    version=0,

    author="Tyler Sedlar",
    author_email="sedlarizona@gmail.com",

    description="A cross-platform status bar made with Qt5",
    license="GNU General Public License v3.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TSedlar/gr8bar",

    packages=setuptools.find_packages(),
    install_requires=['PyQt5'],

    package_data={
        'gr8bar': ['res/*.svg'],
    },

    entry_points={
        'gui_scripts': [
            'gr8bar=gr8bar.gr8bar:main',
        ],
    }
)
