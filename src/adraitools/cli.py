from argparse import ArgumentParser

from adraitools import __version__


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    _ = parser.parse_args()
