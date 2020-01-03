import os
import setuptools
from setuptools import find_packages, setup, Command

here = os.path.abspath(os.path.dirname(__file__))

# Avoids IDE errors, but actual version is read from version.py
__version__ = None
with open("sagas/version.py") as f:
    exec(f.read())

with open("README.md", "r") as fh:
    long_description = fh.read()

# What packages are required for this module to be executed?
REQUIRED = [
    "fire",
    "simplejson",
]

setuptools.setup(
    name="sagas",
    version=__version__,
    author="Samlet Wu",
    author_email="xiaofei.wu@gmail.com",
    description="sagas ai stack",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samlet/stack",
    packages=["", *find_packages(exclude=('actions', 'tests', 'test',
                                          'compose', 'crawlers', 'dart',
                                          'agents', ))],
    entry_points={"console_scripts": ["sagas=sagas.__main__:main"]},
    install_requires=REQUIRED,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_data={
              'conf': ['*'],
              'sagas': ['conf/*'],
              'data': ['synonyms/*']},

    # $ setup.py publish support.
    # cmdclass={
    #     'upload': UploadCommand,
    # },
    project_urls={
        "Bug Reports": "https://github.com/samlet/stack/issues",
        "Source": "https://github.com/samlet/stack",
    },
)

