#!/bin/bash

exec podman run \
    --rm \
    -it \
    -v "$PWD:$PWD" \
    -w "$PWD" \
    --userns keep-id \
    --net=host \
    fedora.help:builder \
    "$@"
