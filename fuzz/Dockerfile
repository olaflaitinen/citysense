# nosemgrep: dockerfile.security.pinned-image
FROM gcr.io/oss-fuzz-base/base-builder-python@sha256:1fd8d37abe830dd3e4b23f9c75a6c5f053307540acf0d4ced621289f709ada6b

RUN pip3 install --no-cache-dir atheris==3.0.0

COPY . /src/citysense
WORKDIR /src/citysense

RUN pip3 install --no-cache-dir .

COPY fuzz/build.sh /src/build.sh
