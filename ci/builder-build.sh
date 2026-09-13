#!/usr/bin/env bash

exec podman build \
    --tag fedora.help:builder \
    -f ci/Containerfile.builder \
    .
