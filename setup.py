#!/usr/bin/env python
"""
Setup package.
"""
import io
from setuptools import setup

# Get long description from readme
with io.open("README.md", "rt", encoding="utf8") as readmefile:
    readme = readmefile.read()

setup(
    name="arm-float-detector",
    version="0.1.0",
    description="Detect software floating point usage in arm binaries",
    author="Noah Pendleton",
    author_email="2538614+noahp@users.noreply.github.com",
    url="https://github.com/noahp/arm-float-detector",
    project_urls={
        "Code": "https://github.com/noahp/arm-float-detector",
        "Issue tracker": "https://github.com/noahp/arm-float-detector/issues",
    },
    long_description=readme,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=["arm_float_detector"],
    entry_points={
        "console_scripts": [
            "arm-float-detector=arm_float_detector.arm_float_detector:main"
        ]
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
)