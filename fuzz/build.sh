#!/bin/bash -eu

pip3 install -e /src/citysense

for fuzzer in /src/citysense/fuzz/fuzz_*.py; do
    fuzzer_basename=$(basename -s .py "$fuzzer")
    compile_python_fuzzer "$fuzzer" --add-data /src/citysense/src/citysense:citysense
done
