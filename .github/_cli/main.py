"""
Main entry point for the CodeAssist CLI.
"""

import click
from rich_click import RichGroup

from .assist import assist
from .config import config
from .workflow import workflow

@click.group(cls=RichGroup)
def main():
    """DevChat - AI-powered coding assistant for developers."""
    pass

# Add command groups
main.add_command(assist)
main.add_command(config)
main.add_command(workflow)

if __name__ == "__main__":
    main() 