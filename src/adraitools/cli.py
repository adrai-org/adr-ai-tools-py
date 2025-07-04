"""Command-line interface for ADR AI Tools."""

from argparse import ArgumentParser

from adraitools import __version__


def main() -> None:
    """Main entry point for the CLI."""
    parser = ArgumentParser()
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.parse_args()
