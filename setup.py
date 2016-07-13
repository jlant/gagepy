#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("CHANGELOG.rst") as changelog_file:
    changelog = changelog_file.read()

with open("LICENSE") as license_file:
    license = license_file.read()


requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    "pytest",
]


setup(
    name="gagepy",
    version="0.1.0",
    description="A Python package that processes and analyzes data files from United States Geological Survey (USGS) streamflow gages.",
    long_description=readme + "\n\n" + changelog,
    author="Jeremiah Lant",
    author_email="jlant@usgs.gov",
    url="",
    packages=[
        "gagepy",
    ],
    package_dir={"gagepy":
                 "gagepy"},
    entry_points={
        "console_scripts": [
            "gagepy = gagepy.cli:main",
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license=license,
    zip_safe=False,
    keywords="gagepy",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
    test_suite="tests",
    tests_require=test_requirements
)
