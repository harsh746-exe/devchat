import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from pathlib import Path
from ..core.config.config import ConfigManager
from ..core.assist.assistant import CodeAssistant
from ..core.test_generation.generator import TestGenerator
from ..core.analysis.analyzer import CodeAnalyzer
from ..core.workflows.workflow import WorkflowManager
from devchat.core.security.analyzer import SecurityAnalyzer
from typing import Optional

console = Console()

@click.group()
@click.version_option()
def cli():
    """DevChat - AI-powered coding assistant"""
    pass

@cli.group()
def assist():
    """AI assistance commands"""
    pass

@cli.group()
def workflow():
    """Workflow management commands"""
    pass

@cli.group()
def config():
    """Configuration management commands"""
    pass

@cli.command()
def security():
    """Security analysis commands"""
    pass

@assist.command()
@click.argument('file_path')
def analyze(file_path):
    """Analyze Python code for improvements"""
    config_manager = ConfigManager()
    config_manager.load_config()
    assistant = CodeAssistant(config_manager.config)
    
    try:
        result = assistant.analyze_code(file_path)
        console.print(Panel.fit(
            Markdown(result['analysis']),
            title=f"Code Analysis for {Path(file_path).name}"
        ))
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@assist.command()
@click.argument('question')
def ask(question):
    """Ask coding questions"""
    config_manager = ConfigManager()
    config_manager.load_config()
    assistant = CodeAssistant(config_manager.config)
    
    try:
        answer = assistant.answer_question(question)
        console.print(Panel.fit(
            Markdown(answer),
            title="Answer"
        ))
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@assist.command()
@click.argument('file_path')
@click.option('--output', '-o', help='Output file path for generated tests')
def generate_tests(file_path, output):
    """Generate tests for Python code"""
    config_manager = ConfigManager()
    config_manager.load_config()
    generator = TestGenerator(config_manager.config)
    
    try:
        test_file = generator.generate_tests(file_path, output)
        if not output:
            console.print(Panel.fit(
                test_file,
                title=f"Generated Tests for {Path(file_path).name}"
            ))
        else:
            console.print(f"[green]Tests generated successfully at {output}[/green]")
            
        # Generate coverage report
        report = generator.generate_coverage_report(file_path, test_file)
        console.print(Panel.fit(
            Markdown(report['report']),
            title="Coverage Report"
        ))
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@assist.command()
@click.argument('file_path')
@click.argument('instructions')
def refactor(file_path, instructions):
    """Refactor Python code"""
    config_manager = ConfigManager()
    config_manager.load_config()
    assistant = CodeAssistant(config_manager.config)
    
    try:
        result = assistant.refactor_code(file_path, instructions)
        console.print(Panel.fit(
            Markdown(result['refactored']),
            title=f"Refactored Code for {Path(file_path).name}"
        ))
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@assist.command()
@click.argument('file_path')
def document(file_path):
    """Generate documentation for Python code"""
    config_manager = ConfigManager()
    config_manager.load_config()
    assistant = CodeAssistant(config_manager.config)
    
    try:
        result = assistant.generate_documentation(file_path)
        console.print(Panel.fit(
            Markdown(result['documentation']),
            title=f"Documentation for {Path(file_path).name}"
        ))
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@workflow.command()
@click.argument('name')
@click.argument('steps_file')
def create(name, steps_file):
    """Create a new workflow"""
    workflow_manager = WorkflowManager()
    
    try:
        workflow_manager.create_workflow(name, steps_file)
        console.print(f"[green]Workflow '{name}' created successfully[/green]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@workflow.command()
def list():
    """List available workflows"""
    workflow_manager = WorkflowManager()
    
    try:
        workflows = workflow_manager.list_workflows()
        table = Table(title="Available Workflows")
        table.add_column("Name", style="cyan")
        table.add_column("Description", style="magenta")
        
        for name in workflows:
            workflow = workflow_manager.get_workflow(name)
            if workflow:
                table.add_row(name, workflow.description)
                
        console.print(table)
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@workflow.command()
@click.argument('name')
@click.argument('file_path')
def run(name, file_path):
    """Run a workflow"""
    workflow_manager = WorkflowManager()
    
    try:
        results = workflow_manager.run_workflow(name, file_path)
        table = Table(title=f"Workflow Results: {name}")
        table.add_column("Step", style="cyan")
        table.add_column("Status", style="magenta")
        table.add_column("Details", style="green")
        
        for step_name, result in results.items():
            table.add_row(
                step_name,
                result.get('status', 'unknown'),
                str(result.get('details', ''))
            )
            
        console.print(table)
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@config.command()
def setup():
    """Set up initial configuration"""
    config_manager = ConfigManager()
    
    try:
        config_manager.setup()
        console.print("[green]Configuration set up successfully[/green]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@config.command()
@click.argument('key')
@click.argument('value')
def set(key, value):
    """Set a configuration value"""
    config_manager = ConfigManager()
    config_manager.load_config()
    
    try:
        config_manager.set(key, value)
        console.print(f"[green]Configuration '{key}' set to '{value}'[/green]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@config.command()
@click.argument('key')
def get(key):
    """Get a configuration value"""
    config_manager = ConfigManager()
    config_manager.load_config()
    
    try:
        value = config_manager.get(key)
        if value:
            console.print(f"[green]{key}: {value}[/green]")
        else:
            console.print(f"[yellow]Configuration '{key}' not found[/yellow]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@config.command()
def list():
    """List all configuration"""
    config_manager = ConfigManager()
    config_manager.load_config()
    
    try:
        config = config_manager.list_all()
        table = Table(title="Configuration")
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="magenta")
        
        for key, value in config.items():
            table.add_row(key, str(value))
            
        console.print(table)
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@security.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file for the security report')
def analyze(file_path: str, output: Optional[str] = None):
    """Analyze a Python file for security vulnerabilities"""
    try:
        analyzer = SecurityAnalyzer(config)
        findings = analyzer.analyze_file(file_path)
        report = analyzer.generate_security_report(findings)
        
        if output:
            with open(output, 'w') as f:
                f.write(report)
            console.print(f"[green]Security report saved to {output}[/green]")
        else:
            console.print(Markdown(report))
            
    except Exception as e:
        console.print(f"[red]Error analyzing file: {str(e)}[/red]")
        raise click.Abort()

@security.command()
@click.argument('file_path', type=click.Path(exists=True))
def suggest_fixes(file_path: str):
    """Suggest fixes for security issues in a file"""
    try:
        analyzer = SecurityAnalyzer(config)
        result = analyzer.suggest_fixes(file_path)
        
        console.print("\n[bold]Security Findings:[/bold]")
        console.print(Markdown(analyzer.generate_security_report(result['findings'])))
        
        console.print("\n[bold]Suggested Fixes:[/bold]")
        console.print(Markdown(result['fixes']))
        
    except Exception as e:
        console.print(f"[red]Error suggesting fixes: {str(e)}[/red]")
        raise click.Abort()

def main():
    cli() 