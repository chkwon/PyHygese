from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext as _build_ext
from setuptools.command.build_py import build_py as _build_py
import subprocess
import os
import platform
from os.path import exists, join as pjoin
import shutil

import urllib.request
urlretrieve = urllib.request.urlretrieve

# try:
#     import urllib.request
#     urlretrieve = urllib.request.urlretrieve
# except ImportError:  # python 2
#     from urllib import urlretrieve


def _run(cmd, cwd):
    subprocess.check_call(cmd, shell=True, cwd=cwd)


def _safe_makedirs(*paths):
    for path in paths:
        try:
            os.makedirs(path)
        except os.error:
            pass


# HGS_VERSION = "0.1.0"
# HGS_SRC = f"https://github.com/chkwon/HGS-CVRP/archive/v{HGS_VERSION}.tar.gz"

HGS_VERSION = "f40c0a465f0df99db3e17c89bf8d9f2f3f0f383a"
HGS_SRC = f"https://github.com/chkwon/HGS-CVRP/archive/{HGS_VERSION}.tar.gz"


LIB_VERSION = "0.0.1"
HGS_CVRP_WIN = f"https://github.com/chkwon/Libhgscvrp_jll.jl/releases/download/libhgscvrp-v{LIB_VERSION}%2B0/" + \
                f"libhgscvrp.v{LIB_VERSION}.x86_64-w64-mingw32-cxx11.tar.gz"

LIB_DIR = "lib"
BUILD_DIR = "lib/build"
BIN_DIR = "lib/bin"


def get_lib_filename():
    if platform.system() == "Linux":
        lib_ext = "so"
    elif platform.system() == "Darwin":
        lib_ext = "dylib"
    elif platform.system() == "Windows":
        lib_ext = "dll"
    else:
        lib_ext = "so"
    return f"libhgscvrp.{lib_ext}"


LIB_FILENAME = get_lib_filename()


def download_build_hgs():
    _safe_makedirs(LIB_DIR)
    _safe_makedirs(BUILD_DIR)
    hgs_src_tarball_name = "{}.tar.gz".format(HGS_VERSION)
    hgs_src_path = pjoin(LIB_DIR, hgs_src_tarball_name)
    urlretrieve(HGS_SRC, hgs_src_path)
    _run(f"tar xzvf {hgs_src_tarball_name}", LIB_DIR)
    _run("cmake -DCMAKE_BUILD_TYPE=Release -G \"Unix Makefiles\" ../HGS-CVRP-{}".format(HGS_VERSION), BUILD_DIR)
    _run("make lib", BUILD_DIR)

    shutil.copyfile(f"{BUILD_DIR}/{LIB_FILENAME}", f"hygese/{LIB_FILENAME}")


def download_binary_hgs():
    print(HGS_CVRP_WIN)

    _safe_makedirs(LIB_DIR)
    dll_tarball_name = "win_bin.tar.gz"
    hgs_bin_path = pjoin(LIB_DIR, dll_tarball_name)
    urlretrieve(HGS_CVRP_WIN, hgs_bin_path)
    _run(f"tar xzvf {dll_tarball_name}", LIB_DIR)
    shutil.copyfile(f"{BIN_DIR}/{LIB_FILENAME}", f"hygese/{LIB_FILENAME}")


class BuildPyCommand(_build_py):
    def run(self):
        print("Build!!!!!! Run!!!!")

        if platform.system() == "Windows":
            # download_binary_hgs()
            download_build_hgs()
        else:
            download_build_hgs()

        _build_py.run(self)


setup(
    name='hygese',
    version='0.0.0.4',
    description='A Python wrapper for the HGS-CVRP solver',
    url='https://github.com/chkwon/PyHygese',
    author='Changhyun Kwon',
    author_email='chkwon@gmail.com',
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
    package_data={
        "": ["libhgscvrp.*"],
    },
    install_requires=["numpy"],
)
