"""
Configuration management command module.
"""

import click
import os
from pathlib import Path
import yaml
from typing import Optional
from loguru import logger

CONFIG_DIR = Path.home() / ".devchat"
CONFIG_FILE = CONFIG_DIR / "config.yaml"

def ensure_config_dir():
    """Ensure the configuration directory exists."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def load_config() -> dict:
    """Load the configuration file."""
    ensure_config_dir()
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return yaml.safe_load(f) or {}
    return {}

def save_config(config: dict):
    """Save the configuration file."""
    ensure_config_dir()
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f)

@click.group()
def config():
    """Configuration management commands."""
    pass

@config.command()
@click.argument('key')
@click.argument('value')
def set(key: str, value: str):
    """Set a configuration value."""
    try:
        config = load_config()
        config[key] = value
        save_config(config)
        click.echo(f"Set {key} = {value}")
    except Exception as e:
        logger.error(f"Error setting configuration: {str(e)}")
        raise click.ClickException(str(e))

@config.command()
@click.argument('key')
def get(key: str):
    """Get a configuration value."""
    try:
        config = load_config()
        value = config.get(key)
        if value is None:
            click.echo(f"Configuration key '{key}' not found")
        else:
            click.echo(value)
    except Exception as e:
        logger.error(f"Error getting configuration: {str(e)}")
        raise click.ClickException(str(e))

@config.command()
@click.argument('key')
def unset(key: str):
    """Remove a configuration value."""
    try:
        config = load_config()
        if key in config:
            del config[key]
            save_config(config)
            click.echo(f"Removed {key}")
        else:
            click.echo(f"Configuration key '{key}' not found")
    except Exception as e:
        logger.error(f"Error removing configuration: {str(e)}")
        raise click.ClickException(str(e))

@config.command()
def list():
    """List all configuration values."""
    try:
        config = load_config()
        if not config:
            click.echo("No configuration values set")
            return
            
        click.echo("\nConfiguration:")
        click.echo("=============")
        for key, value in config.items():
            click.echo(f"{key}: {value}")
    except Exception as e:
        logger.error(f"Error listing configuration: {str(e)}")
        raise click.ClickException(str(e))

@config.command()
@click.option('--api-key', prompt=True, hide_input=True, help='OpenAI API key')
def setup(api_key: str):
    """Setup initial configuration."""
    try:
        config = {
            'openai_api_key': api_key,
            'model': 'gpt-4',
            'temperature': 0.7
        }
        save_config(config)
        click.echo("Configuration setup complete")
    except Exception as e:
        logger.error(f"Error setting up configuration: {str(e)}")
        raise click.ClickException(str(e)) 