"""
Code assistance command module.
"""

import click
from pathlib import Path
from typing import Optional
import asyncio
from loguru import logger

from ..ai.engine import AIEngine
from ..analyzer.code_analyzer import CodeAnalyzer

@click.group()
def assist():
    """Code assistance commands."""
    pass

@assist.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--context', '-c', help='Additional context for the analysis')
def analyze(file_path: str, context: Optional[str] = None):
    """Analyze a Python file."""
    try:
        analyzer = CodeAnalyzer()
        result = analyzer.analyze_file(file_path)
        
        click.echo("\nCode Analysis Results:")
        click.echo("=====================")
        
        # Display complexity metrics
        click.echo("\nComplexity Metrics:")
        click.echo(f"Cyclomatic Complexity: {result['complexity']['cyclomatic']}")
        click.echo(f"Cognitive Complexity: {result['complexity']['cognitive']}")
        click.echo(f"Lines of Code: {result['complexity']['lines']}")
        
        # Display imports
        if result['imports']:
            click.echo("\nImports:")
            for imp in result['imports']:
                if imp['type'] == 'import':
                    alias = f" as {imp['alias']}" if imp.get('alias') else ''
                    click.echo(f"import {imp['module']}{alias}")
                else:
                    alias = f" as {imp['alias']}" if imp.get('alias') else ''
                    click.echo(f"from {imp['module']} import {imp['name']}{alias}")
        
        # Display functions
        if result['functions']:
            click.echo("\nFunctions:")
            for func in result['functions']:
                click.echo(f"\n{func['name']}({', '.join(func['args'])})")
                if func['returns']:
                    click.echo(f"Returns: {func['returns']}")
                if func['docstring']:
                    click.echo(f"Docstring: {func['docstring']}")
        
        # Display classes
        if result['classes']:
            click.echo("\nClasses:")
            for cls in result['classes']:
                click.echo(f"\nclass {cls['name']}({', '.join(cls['bases'])})")
                if cls['docstring']:
                    click.echo(f"Docstring: {cls['docstring']}")
                click.echo("Methods:")
                for method in cls['methods']:
                    click.echo(f"  - {method}")
                    
    except Exception as e:
        logger.error(f"Error analyzing file: {str(e)}")
        raise click.ClickException(str(e))

@assist.command()
@click.argument('query')
@click.option('--file', '-f', type=click.Path(exists=True), help='File to provide context')
@click.option('--model', '-m', default='gpt-4', help='Model to use for completion')
async def ask(query: str, file: Optional[str] = None, model: str = 'gpt-4'):
    """Ask a coding question."""
    try:
        api_key = click.prompt('Enter your OpenAI API key', hide_input=True)
        engine = AIEngine(api_key, model)
        
        context = None
        if file:
            with open(file, 'r') as f:
                context = f.read()
        
        response = await engine.get_completion([
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}" if context else query}
        ])
        
        click.echo("\nResponse:")
        click.echo("=========")
        click.echo(response)
        
    except Exception as e:
        logger.error(f"Error getting response: {str(e)}")
        raise click.ClickException(str(e))

@assist.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file for generated tests')
async def generate_tests(file_path: str, output: Optional[str] = None):
    """Generate tests for a Python file."""
    try:
        api_key = click.prompt('Enter your OpenAI API key', hide_input=True)
        engine = AIEngine(api_key)
        
        with open(file_path, 'r') as f:
            code = f.read()
        
        response = await engine.get_completion([
            {"role": "system", "content": "You are a test generation expert. Generate comprehensive unit tests."},
            {"role": "user", "content": f"Generate unit tests for this code:\n\n{code}"}
        ])
        
        if output:
            with open(output, 'w') as f:
                f.write(response)
            click.echo(f"Tests written to {output}")
        else:
            click.echo("\nGenerated Tests:")
            click.echo("===============")
            click.echo(response)
            
    except Exception as e:
        logger.error(f"Error generating tests: {str(e)}")
        raise click.ClickException(str(e)) 