#!/bin/bash -eu

pip3 install --no-cache-dir /src/citysense

for fuzzer in /src/citysense/fuzz/fuzz_*.py; do
    compile_python_fuzzer "$fuzzer"
done
