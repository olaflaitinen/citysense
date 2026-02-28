FROM gcr.io/oss-fuzz-base/base-builder-python

RUN pip3 install atheris

COPY . /src/citysense
WORKDIR /src/citysense

RUN pip3 install -e .

COPY fuzz/build.sh /src/build.sh
