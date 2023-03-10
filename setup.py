from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext as _build_ext
from setuptools.command.build_py import build_py as _build_py

from distutils.core import setup, Extension
from Cython.Build import cythonize

import subprocess
import os
import platform
from os.path import exists, join as pjoin
import shutil

import urllib.request

urlretrieve = urllib.request.urlretrieve

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


def _run(cmd, cwd):
    subprocess.check_call(cmd, shell=True, cwd=cwd)


def _safe_makedirs(*paths):
    for path in paths:
        try:
            os.makedirs(path)
        except os.error:
            pass


HGS_VERSION = "2.0.0"
HGS_SRC = f"https://github.com/vidalt/HGS-CVRP/archive/v{HGS_VERSION}.tar.gz"

LIB_DIR = "deps"
BUILD_DIR = "deps/build"
BIN_DIR = "deps/bin"


def get_lib_filename():
    sysname = platform.system()
    if sysname == "Linux":
        lib_ext = "so"
    elif sysname == "Darwin":
        lib_ext = "dylib"
    elif sysname == "Windows":
        lib_ext = "dll"
    else:
        raise ValueError("Unknown platform: " + sysname)
    return f"libhgscvrp.{lib_ext}"

def get_rpath_arg():
    sysname = platform.system()
    if sysname == "Linux":
        return "-Wl,-rpath,$ORIGIN/usr/local/lib"
    elif sysname == "Darwin":
        return "-Wl,-rpath,@loader_path/usr/local/lib"
    elif sysname == "Windows":
        return ""
    else:
        raise ValueError("Unknown platform: " + sysname)


LIB_FILENAME = get_lib_filename()


def download_build_hgs():
    _safe_makedirs(LIB_DIR)
    _safe_makedirs(BUILD_DIR)
    hgs_src_tarball_name = "{}.tar.gz".format(HGS_VERSION)
    hgs_src_path = pjoin(LIB_DIR, hgs_src_tarball_name)
    urlretrieve(HGS_SRC, hgs_src_path)
    _run(f"tar xzvf {hgs_src_tarball_name}", LIB_DIR)
    _run(
        f'cmake -DCMAKE_BUILD_TYPE=Release -G "Unix Makefiles" ../HGS-CVRP-{HGS_VERSION}',
        BUILD_DIR,
    )
    _run("make lib", BUILD_DIR)
    _run("make DESTDIR=../../hygese install", BUILD_DIR)

    # shutil.copyfile(f"{BUILD_DIR}/{LIB_FILENAME}", f"hygese/{LIB_FILENAME}")


class BuildPyCommand(_build_py):
    def run(self):
        download_build_hgs()
        _build_py.run(self)




CDIR = os.path.dirname(os.path.abspath(__file__))

extentions = [
    Extension(
        name="hygese.wrapper",
        sources=["hygese/wrapper.pyx"],
        include_dirs = ["hygese/usr/local/include"],
        library_dirs = ["hygese/usr/local/lib"],
        libraries = ["hgscvrp"],
        extra_link_args = [get_rpath_arg()]
    )
]




setup(
    name="hygese",
    version="0.0.1.0",
    description="A Python wrapper for the HGS-CVRP solver",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chkwon/PyHygese",
    author="Changhyun Kwon",
    author_email="chkwon@gmail.com",
    project_urls={
        "Bug Tracker": "https://github.com/chkwon/PyHygese/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=find_packages(),
    python_requires=">=3.6",
    cmdclass={
        "build_py": BuildPyCommand,
    },
    ext_modules=extentions,    
    # data_files=[("lib", [f"hygese/{LIB_FILENAME}"])],
    include_package_data=True,    
    package_data={
        "hygese": ["usr/local/lib/*.so", "usr/local/lib/*.dylib", "usr/local/include/*.h"],
    },
    install_requires=[
        "Cython>=0.29.0",
        "numpy>=1.23.0",
    ],
)
