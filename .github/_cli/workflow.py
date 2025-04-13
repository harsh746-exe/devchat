"""
Workflow management command module.
"""

import click
import yaml
from pathlib import Path
from typing import Optional
from loguru import logger

from ..workflow.manager import WorkflowManager

@click.group()
def workflow():
    """Workflow management commands."""
    pass

@workflow.command()
@click.argument('name')
@click.option('--description', '-d', help='Workflow description')
@click.option('--steps', '-s', help='YAML file containing workflow steps')
def create(name: str, description: Optional[str] = None, steps: Optional[str] = None):
    """Create a new workflow."""
    try:
        manager = WorkflowManager()
        
        workflow_data = {
            'name': name,
            'description': description or f"Workflow: {name}",
            'steps': []
        }
        
        if steps:
            with open(steps, 'r') as f:
                workflow_data['steps'] = yaml.safe_load(f)
        
        manager.add_workflow(name, workflow_data)
        click.echo(f"Created workflow: {name}")
    except Exception as e:
        logger.error(f"Error creating workflow: {str(e)}")
        raise click.ClickException(str(e))

@workflow.command()
@click.argument('name')
def remove(name: str):
    """Remove a workflow."""
    try:
        manager = WorkflowManager()
        manager.remove_workflow(name)
        click.echo(f"Removed workflow: {name}")
    except Exception as e:
        logger.error(f"Error removing workflow: {str(e)}")
        raise click.ClickException(str(e))

@workflow.command()
def list():
    """List all workflows."""
    try:
        manager = WorkflowManager()
        workflows = manager.list_workflows()
        
        if not workflows:
            click.echo("No workflows found")
            return
            
        click.echo("\nWorkflows:")
        click.echo("==========")
        for name in workflows:
            workflow = manager.get_workflow(name)
            click.echo(f"\n{name}")
            click.echo(f"Description: {workflow['description']}")
            click.echo(f"Steps: {len(workflow['steps'])}")
    except Exception as e:
        logger.error(f"Error listing workflows: {str(e)}")
        raise click.ClickException(str(e))

@workflow.command()
@click.argument('name')
@click.option('--file', '-f', type=click.Path(exists=True), help='File to process')
@click.option('--output', '-o', type=click.Path(), help='Output file')
def run(name: str, file: Optional[str] = None, output: Optional[str] = None):
    """Run a workflow."""
    try:
        manager = WorkflowManager()
        workflow = manager.get_workflow(name)
        
        if not workflow:
            raise click.ClickException(f"Workflow '{name}' not found")
            
        kwargs = {}
        if file:
            kwargs['file'] = file
        if output:
            kwargs['output'] = output
            
        results = manager.execute_workflow(name, **kwargs)
        
        click.echo("\nWorkflow Results:")
        click.echo("================")
        for key, value in results.items():
            click.echo(f"\n{key}:")
            click.echo(value)
    except Exception as e:
        logger.error(f"Error running workflow: {str(e)}")
        raise click.ClickException(str(e))

@workflow.command()
@click.argument('name')
@click.argument('steps_file', type=click.Path(exists=True))
def update(name: str, steps_file: str):
    """Update workflow steps."""
    try:
        manager = WorkflowManager()
        workflow = manager.get_workflow(name)
        
        if not workflow:
            raise click.ClickException(f"Workflow '{name}' not found")
            
        with open(steps_file, 'r') as f:
            new_steps = yaml.safe_load(f)
            
        workflow['steps'] = new_steps
        manager.add_workflow(name, workflow)
        click.echo(f"Updated workflow: {name}")
    except Exception as e:
        logger.error(f"Error updating workflow: {str(e)}")
        raise click.ClickException(str(e)) 