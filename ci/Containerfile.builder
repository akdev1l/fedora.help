FROM registry.fedoraproject.org/fedora:44

RUN dnf install -y \
    git \
    python3 \
    poetry
