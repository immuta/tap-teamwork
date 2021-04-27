#!/usr/bin/env python
import setuptools

setuptools.setup(
    name="tap-teamwork",
    version="0.3.0",
    description="Singer.io tap for extracting data",
    author="Stephen Bailey",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    packages=setuptools.find_packages(),
    py_modules=["tap_teamwork"],
    package_data={"schemas": ["tap_teamwork/schemas/*.json"]},
    entry_points="""
        [console_scripts]
        tap-teamwork=tap_teamwork.tap:cli
    """,
    install_requires=["singer-sdk"],
    include_package_data=True,
)
