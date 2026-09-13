#!/usr/bin/env python

from logging import getLogger, basicConfig, INFO
from subprocess import run
from sys import argv

basicConfig(
    level=INFO,
    format='[%(asctime)s] (%(levelname)s): %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S'
)
log = getLogger(__name__)

def main():
    log.info("Hello World!")
    run([
        "poetry",
        "run",
        "mkdocs",
        *argv
    ])


if __name__ == '__main__':
    main()
