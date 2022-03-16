# https://packaging.python.org/en/latest/tutorials/packaging-projects/
# https://lsjsj92.tistory.com/592
# pip install git+https://github.com/chkwon/pyfun
# https://jichu4n.com/posts/how-to-add-custom-build-steps-and-commands-to-setuppy/

from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext as _build_ext
from setuptools.command.build_py import build_py as _build_py
import subprocess
import os
import platform
from os.path import exists, join as pjoin
import shutil

try:
    import urllib.request
    urlretrieve = urllib.request.urlretrieve
except ImportError:  # python 2
    from urllib import urlretrieve


def _run(cmd, cwd):
    subprocess.check_call(cmd, shell=True, cwd=cwd)
def _safe_makedirs(*paths):
    for path in paths:
        try:
            os.makedirs(path)
        except os.error:
            pass

HGS_VERSION = "c_interface"
HGS_SRC = "https://github.com/chkwon/HGS-CVRP/archive/refs/heads/{}.tar.gz".format(HGS_VERSION)

HGS_CVRP_WIN = "https://github.com/chkwon/HGS_CVRP_jll.jl/releases/download/libhgscvrp-v0.1.0%2B0/libhgscvrp.v0.1.0.x86_64-w64-mingw32-cxx11.tar.gz"

def download_build_hgs():
    if platform.system() == "Linux":
        lib_ext = "so"
    elif platform.system() == "Darwin":
        lib_ext = "dylib"
    elif platform.system() == "Windows":
        lib_ext = "dll"
    else:
        lib_ext = "so"

        
    lib_filename = "libhgscvrp.{}".format(lib_ext)

    _safe_makedirs("lib")
    _safe_makedirs("lib/build")
    hgs_src_tarball_name = "{}.tar.gz".format(HGS_VERSION)
    hgs_src_path = pjoin("lib", hgs_src_tarball_name)
    urlretrieve(HGS_SRC, hgs_src_path)
    _run("tar xzvf {}".format(hgs_src_tarball_name), "lib")
    _run("cmake -DCMAKE_BUILD_TYPE=Release ../HGS-CVRP-{}".format(HGS_VERSION), "lib/build")
    _run("make", "lib/build")
    _run("cp {} ../../src/hgs/".format(lib_filename), "lib/build")


def download_binary_hgs():
    _safe_makedirs("lib")
    hgs_bin_path = pjoin("lib", "win_bin.tar.gz")
    urlretrieve(HGS_CVRP_WIN, hgs_bin_path)
    _run("tar xzvf win_bin.tar.gz", "lib")
    shutil.copyfile("lib/bin/libhgscvrp.dll", "src/hgs/libhgscvrp.dll")
    shutil.copyfile("lib/bin/libhgscvrp.dll.a", "src/hgs/libhgscvrp.dll.a")

class BuildPyCommand(_build_py):
    def run(self):
        print("Build!!!!!! Run!!!!")   

        if platform.system() == "Windows":
            download_binary_hgs()
        else:
            download_build_hgs()
            
        _build_py.run(self)



setup(
    name='hgs',
    version='0.1',
    description='A Python wrapper for the HGS-CVRP solver',
    url='https://github.com/chkwon/pyhgscvrp',
    author='Changhyun Kwon',
    author_email='chkwon@gmail.com',
    project_urls={
        "Bug Tracker": "https://github.com/chkwon/pyhgscvrp/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],    
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    cmdclass={
        "build_py": BuildPyCommand,
    },    
    package_data={
        "hgs": ["libhgscvrp.*"],
    },
    install_requires=["numpy"],
)