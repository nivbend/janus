"""Setuptools setup script for the package."""

from setuptools import setup

def _get_version():
    # pylint: disable=missing-docstring
    with open(".version") as version:
        return version.read().rstrip("\n")

setup(
    name = "janus",
    version = _get_version(),
    description = "A access manager for scarce resources",
    url = "http://gitlab.com/nivbend/janus",
    author = "Niv Ben-David",
    author_email = "nivbend@gmail.com",
    license = "MIT",
    packages = ["janus", ],
    install_requires = [
    ],
    classifiers = [
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Software Development :: Testing",
    ],
    keywords = [
        "resource",
        "resources",
    ])
