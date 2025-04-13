import ast
from typing import List, Dict, Optional
from pathlib import Path
import importlib.util
import inspect
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class TestGenerator:
    """Generates test cases for Python code"""
    
    def __init__(self, config):
        self.config = config
        self.llm = ChatOpenAI(
            model_name=config.model,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            api_key=config.api_key
        )
        self.test_template = """import pytest
from {module_name} import {imports}

{test_cases}
"""
        
    def generate_tests(self, file_path: str, output_path: Optional[str] = None) -> str:
        """Generate test cases for a Python file"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        # Parse the file
        with open(file_path, 'r') as f:
            source = f.read()
            tree = ast.parse(source)
            
        # Get module name
        module_name = path.stem
        
        # Find functions and classes to test
        testable_objects = self._find_testable_objects(tree)
        
        # Generate test cases using AI
        test_cases = []
        for obj in testable_objects:
            if obj['type'] == 'function':
                test_case = self._generate_function_test_with_ai(obj, source)
            else:
                test_case = self._generate_class_test_with_ai(obj, source)
            test_cases.append(test_case)
        
        # Format the test file
        test_file = self.test_template.format(
            module_name=module_name,
            imports=', '.join(obj['name'] for obj in testable_objects),
            test_cases='\n\n'.join(test_cases)
        )
        
        # Write to output file if specified
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(test_file)
                
        return test_file
        
    def _find_testable_objects(self, tree: ast.AST) -> List[Dict]:
        """Find functions and classes that should be tested"""
        testable_objects = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                # Skip private methods and classes
                if not node.name.startswith('_'):
                    testable_objects.append({
                        'name': node.name,
                        'type': 'function' if isinstance(node, ast.FunctionDef) else 'class',
                        'node': node
                    })
                    
        return testable_objects
        
    def _generate_function_test_with_ai(self, obj: Dict, source: str) -> str:
        """Generate test case for a function using AI"""
        prompt = ChatPromptTemplate.from_template("""
        Generate comprehensive test cases for the following Python function:
        
        Function: {function_name}
        Code:
        {code}
        
        Include:
        1. Test cases for normal operation
        2. Edge cases and error conditions
        3. Input validation
        4. Expected outputs
        5. Mocking if needed
        
        Return the test cases in pytest format with detailed comments.
        """)
        
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({
            "function_name": obj['name'],
            "code": source
        })
        
    def _generate_class_test_with_ai(self, obj: Dict, source: str) -> str:
        """Generate test case for a class using AI"""
        prompt = ChatPromptTemplate.from_template("""
        Generate comprehensive test cases for the following Python class:
        
        Class: {class_name}
        Code:
        {code}
        
        Include:
        1. Test cases for initialization
        2. Test cases for all public methods
        3. Edge cases and error conditions
        4. Property testing
        5. Mocking if needed
        
        Return the test cases in pytest format with detailed comments.
        """)
        
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({
            "class_name": obj['name'],
            "code": source
        })
        
    def generate_coverage_report(self, file_path: str, test_file: str) -> Dict:
        """Generate a coverage report for the test file"""
        prompt = ChatPromptTemplate.from_template("""
        Analyze the following Python code and its test file to generate a coverage report:
        
        Original code:
        {code}
        
        Test file:
        {test_file}
        
        Provide a detailed coverage report including:
        1. Lines covered
        2. Lines not covered
        3. Branch coverage
        4. Suggestions for additional test cases
        5. Potential edge cases not covered
        """)
        
        with open(file_path, 'r') as f:
            code = f.read()
            
        chain = prompt | self.llm | StrOutputParser()
        report = chain.invoke({
            "code": code,
            "test_file": test_file
        })
        
        return {
            "report": report,
            "file": file_path
        } 