from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Polyharmonic spline interpolation in PyTorch'

# Setting up
setup(
    name="torchrbf",
    version=VERSION,
    author="Arman Maesumi",
    author_email="arman.maesumi@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'pytorch', 'rbf', 'interpolation', 'radial basis function'],
    classifiers=[]
)



import io
import re

from setuptools import setup
from setuptools import find_packages


# PyCOMET info
file = open('pycomet/__init__.py').read()
info = {}
for k in ("author", "email", "url", "license", "version"):
  info[k] = re.search(
    r"^__{0}__ = ['\"]([^'\"]*)['\"]".format(k), file, re.M
  ).group(1)

# Description
description = 'Polyharmonic spline interpolation in PyTorch'

# Dependencies
with open("requirements.txt", "r") as f:
  install_requires = [x.strip() for x in f.readlines()]

# Info
with io.open("README.md", "r", encoding="utf-8") as f:
  long_description = f.read()

classifiers = [
  "Development Status :: 1 - Beta",
  "Intended Audience :: Developers",
  "Intended Audience :: Education",
  "Intended Audience :: Science/Research",
  "License :: OSI Approved :: MIT License",
  "Programming Language :: Python :: 3",
  "Topic :: Scientific/Engineering",
  "Topic :: Scientific/Engineering :: Mathematics",
  "Topic :: Software Development :: Libraries",
  "Topic :: Software Development :: Libraries :: Python Modules"
]

keywords = [
  "Python",
  "PyTorch",
  "Interpolation",
  "Spline",
  "Polyharmonic Spline",
  "RBF",
  "Radial Basis Function",
]

setup(
  name="pycomet",
  version=info["version"],
  description=description,
  long_description=long_description,
  long_description_content_type="text/markdown",
  author=info["author"],
  author_email=info["email"],
  url=info["url"],
  license=info["license"],
  install_requires=install_requires,
  classifiers=classifiers,
  keywords=keywords,
  packages=find_packages(),
  include_package_data=True,
  python_requires=">=3.8",
)
