"""Defines the main entrypoint for Milton."""

# Standard library imports.
from sys import exit

# Local imports.
from milton.server import Server


def main():
    server = Server(
        name="milton",
        llm_tag="openai"
    )
    server.Start()

if __name__ == "__main__":
    exit(main())
