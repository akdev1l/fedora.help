FROM registry.fedoraproject.org/fedora:44

RUN dnf install -y \
    python3 \
    poetry
