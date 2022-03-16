# pyhgscvrp

A Python wrapper for [HGS-CVRP](https://github.com/vidalt/HGS-CVRP).

Installation requires a `C++` compiler and `cmake` tool.
```
git clone git@github.com:chkwon/HGS-CVRP.git
cd HGS-CVRP
git checkout c_interface
mkdir build
cd build 
cmake -DCMAKE_BUILD_TYPE=Release ../
make
```

The generated shared library file `libhgscvrp.dylib`, `libhgscvrp.so`, or `libhgscvrp.dll` should be found in `\build`.

Open `hgs.py` in this repository and edit `HGS_LIBRARY_FILEPATH` to the `libhgscvrp` shared library file location.

Examples:
```
python3 example_tsp.py
python3 example_cvrp.py
```

