import ast
from typing import Dict, List, Optional
from pathlib import Path
import astroid
from pylint.lint import Run
from pylint.reporters.text import TextReporter
import io

class CodeAnalyzer:
    """Analyzes Python code for improvements"""
    
    def __init__(self):
        self.pylint_output = io.StringIO()
        self.reporter = TextReporter(self.pylint_output)
        
    def analyze_file(self, file_path: str) -> Dict:
        """Analyze a Python file for improvements"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        # Run pylint analysis
        Run([str(path)], reporter=self.reporter, do_exit=False)
        pylint_results = self.pylint_output.getvalue()
        
        # Parse the file for additional analysis
        with open(file_path, 'r') as f:
            source = f.read()
            tree = ast.parse(source)
            
        # Basic metrics
        metrics = {
            'lines_of_code': len(source.splitlines()),
            'functions': len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]),
            'classes': len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]),
            'imports': len([node for node in ast.walk(tree) if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom)]),
        }
        
        # Complexity analysis
        try:
            astroid_tree = astroid.parse(source)
            complexity = self._calculate_complexity(astroid_tree)
            metrics['complexity'] = complexity
        except Exception as e:
            metrics['complexity'] = f"Error calculating complexity: {str(e)}"
            
        return {
            'metrics': metrics,
            'pylint_results': pylint_results,
            'suggestions': self._generate_suggestions(metrics, pylint_results)
        }
        
    def _calculate_complexity(self, node: astroid.nodes.NodeNG) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1
        for child in node.get_children():
            if isinstance(child, (astroid.nodes.If, astroid.nodes.For, astroid.nodes.While,
                                astroid.nodes.TryExcept, astroid.nodes.TryFinally)):
                complexity += 1
            complexity += self._calculate_complexity(child)
        return complexity
        
    def _generate_suggestions(self, metrics: Dict, pylint_results: str) -> List[str]:
        """Generate improvement suggestions based on analysis"""
        suggestions = []
        
        # Complexity suggestions
        if 'complexity' in metrics and isinstance(metrics['complexity'], int):
            if metrics['complexity'] > 10:
                suggestions.append("Consider breaking down complex functions into smaller, more manageable pieces")
                
        # Function count suggestions
        if metrics['functions'] > 20:
            suggestions.append("Consider splitting the file into multiple modules")
            
        # Import suggestions
        if metrics['imports'] > 10:
            suggestions.append("Consider organizing imports and removing unused ones")
            
        # Add pylint suggestions
        if "error" in pylint_results.lower():
            suggestions.append("Fix the errors reported by pylint")
            
        return suggestions 