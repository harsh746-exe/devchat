"""
Code analysis utilities.
"""

import os
import ast
from typing import Dict, List, Any, Optional
import tokenize
from io import StringIO
from pathlib import Path
from loguru import logger

class CodeAnalyzer:
    def __init__(self):
        """Initialize the code analyzer."""
        pass

    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a Python file.
        
        Args:
            file_path: Path to the Python file
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            return self.analyze_code(content, file_path)
        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {str(e)}")
            raise

    def analyze_code(self, code: str, file_path: Optional[str] = None) -> Dict[str, Any]:
        """Analyze Python code.
        
        Args:
            code: Python code to analyze
            file_path: Optional path to the file (for context)
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            tree = ast.parse(code)
            return {
                'complexity': self._calculate_complexity(tree),
                'imports': self._analyze_imports(tree),
                'functions': self._analyze_functions(tree),
                'classes': self._analyze_classes(tree),
                'file_path': file_path
            }
        except Exception as e:
            logger.error(f"Error analyzing code: {str(e)}")
            raise

    def _calculate_complexity(self, tree: ast.AST) -> Dict[str, int]:
        """Calculate code complexity metrics.
        
        Args:
            tree: AST of the code
            
        Returns:
            Dictionary of complexity metrics
        """
        complexity = {
            'cyclomatic': 0,
            'cognitive': 0,
            'lines': len(ast.unparse(tree).split('\n'))
        }

        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.Try, ast.ExceptHandler)):
                complexity['cyclomatic'] += 1
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                complexity['cognitive'] += 1

        return complexity

    def _analyze_imports(self, tree: ast.AST) -> List[Dict[str, str]]:
        """Analyze imports in the code.
        
        Args:
            tree: AST of the code
            
        Returns:
            List of import information
        """
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imports.append({
                        'module': name.name,
                        'alias': name.asname,
                        'type': 'import'
                    })
            elif isinstance(node, ast.ImportFrom):
                for name in node.names:
                    imports.append({
                        'module': node.module,
                        'name': name.name,
                        'alias': name.asname,
                        'type': 'from_import'
                    })
        return imports

    def _analyze_functions(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Analyze functions in the code.
        
        Args:
            tree: AST of the code
            
        Returns:
            List of function information
        """
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    'name': node.name,
                    'args': [arg.arg for arg in node.args.args],
                    'returns': self._get_return_type(node),
                    'docstring': ast.get_docstring(node),
                    'complexity': self._calculate_complexity(node)
                })
        return functions

    def _analyze_classes(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Analyze classes in the code.
        
        Args:
            tree: AST of the code
            
        Returns:
            List of class information
        """
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append({
                    'name': node.name,
                    'bases': [base.id for base in node.bases if isinstance(base, ast.Name)],
                    'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)],
                    'docstring': ast.get_docstring(node)
                })
        return classes

    def _get_return_type(self, node: ast.FunctionDef) -> Optional[str]:
        """Get the return type annotation of a function.
        
        Args:
            node: Function definition node
            
        Returns:
            Return type as string if annotated, None otherwise
        """
        if node.returns:
            return ast.unparse(node.returns)
        return None

    @staticmethod
    def read_file(file_path: str) -> str:
        """Read a file and return its contents."""
        with open(file_path, 'r') as f:
            return f.read()

    @staticmethod
    def extract_functions(code: str) -> List[Dict]:
        """Extract function definitions from code."""
        try:
            tree = ast.parse(code)
            functions = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        'name': node.name,
                        'lineno': node.lineno,
                        'args': [arg.arg for arg in node.args.args],
                        'docstring': ast.get_docstring(node)
                    })
            
            return functions
        except Exception as e:
            return []

    @staticmethod
    def extract_classes(code: str) -> List[Dict]:
        """Extract class definitions from code."""
        try:
            tree = ast.parse(code)
            classes = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    methods = []
                    for child in node.body:
                        if isinstance(child, ast.FunctionDef):
                            methods.append({
                                'name': child.name,
                                'lineno': child.lineno,
                                'args': [arg.arg for arg in child.args.args],
                                'docstring': ast.get_docstring(child)
                            })
                    
                    classes.append({
                        'name': node.name,
                        'lineno': node.lineno,
                        'methods': methods,
                        'docstring': ast.get_docstring(node)
                    })
            
            return classes
        except Exception as e:
            return []

    @staticmethod
    def get_imports(code: str) -> List[Dict]:
        """Extract import statements from code."""
        try:
            tree = ast.parse(code)
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imports.append({
                            'name': name.name,
                            'asname': name.asname,
                            'lineno': node.lineno,
                            'type': 'import'
                        })
                elif isinstance(node, ast.ImportFrom):
                    for name in node.names:
                        imports.append({
                            'name': name.name,
                            'asname': name.asname,
                            'module': node.module,
                            'lineno': node.lineno,
                            'type': 'from'
                        })
            
            return imports
        except Exception as e:
            return []

    @staticmethod
    def analyze_complexity(code: str) -> Dict:
        """Analyze code complexity."""
        try:
            tree = ast.parse(code)
            stats = {
                'num_functions': 0,
                'num_classes': 0,
                'num_imports': 0,
                'lines_of_code': len(code.splitlines()),
                'complexity_score': 0
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    stats['num_functions'] += 1
                    # Basic complexity scoring
                    stats['complexity_score'] += len(list(ast.walk(node)))
                elif isinstance(node, ast.ClassDef):
                    stats['num_classes'] += 1
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    stats['num_imports'] += 1
            
            return stats
        except Exception as e:
            return {
                'error': str(e)
            }

    @staticmethod
    def find_todos(code: str) -> List[Dict]:
        """Find TODO comments in code."""
        todos = []
        try:
            lines = StringIO(code).readlines()
            for i, line in enumerate(lines, 1):
                if 'TODO' in line or 'FIXME' in line:
                    todos.append({
                        'line': i,
                        'content': line.strip(),
                        'type': 'TODO' if 'TODO' in line else 'FIXME'
                    })
            return todos
        except Exception as e:
            return [] 