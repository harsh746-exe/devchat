from typing import Dict, List, Optional
from pathlib import Path
import ast
import networkx as nx
import matplotlib.pyplot as plt
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class CodeVisualizer:
    """Visualizes Python code structure and relationships"""
    
    def __init__(self, config):
        self.config = config
        self.llm = ChatOpenAI(
            model_name=config.model,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            api_key=config.api_key
        )
        
    def generate_call_graph(self, file_path: str, output_path: Optional[str] = None) -> Dict:
        """Generate a call graph visualization"""
        with open(file_path, 'r') as f:
            code = f.read()
            tree = ast.parse(code)
            
        G = nx.DiGraph()
        
        # Extract function calls
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                function_name = node.name
                G.add_node(function_name)
                
                for child in ast.walk(node):
                    if isinstance(child, ast.Call):
                        if isinstance(child.func, ast.Name):
                            called_function = child.func.id
                            G.add_edge(function_name, called_function)
                            
        # Generate visualization
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', 
                node_size=2000, font_size=10, font_weight='bold')
                
        if output_path:
            plt.savefig(output_path)
            plt.close()
            
        return {
            "graph": G,
            "file": file_path,
            "output": output_path
        }
        
    def generate_class_diagram(self, file_path: str, output_path: Optional[str] = None) -> Dict:
        """Generate a class diagram visualization"""
        with open(file_path, 'r') as f:
            code = f.read()
            tree = ast.parse(code)
            
        G = nx.DiGraph()
        
        # Extract class relationships
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                G.add_node(class_name)
                
                # Check for inheritance
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        parent_class = base.id
                        G.add_edge(class_name, parent_class)
                        
        # Generate visualization
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightgreen',
                node_size=2000, font_size=10, font_weight='bold')
                
        if output_path:
            plt.savefig(output_path)
            plt.close()
            
        return {
            "graph": G,
            "file": file_path,
            "output": output_path
        }
        
    def generate_code_explanation(self, file_path: str) -> Dict:
        """Generate a natural language explanation of the code"""
        with open(file_path, 'r') as f:
            code = f.read()
            
        prompt = ChatPromptTemplate.from_template("""
        Explain the following Python code in a way that's easy to understand:
        
        Code:
        {code}
        
        Provide:
        1. A high-level overview of what the code does
        2. Explanation of key functions and classes
        3. Data flow and relationships
        4. Important algorithms or patterns used
        5. Potential improvements or considerations
        """)
        
        chain = prompt | self.llm | StrOutputParser()
        explanation = chain.invoke({"code": code})
        
        return {
            "explanation": explanation,
            "file": file_path
        }
        
    def generate_complexity_heatmap(self, file_path: str, output_path: Optional[str] = None) -> Dict:
        """Generate a complexity heatmap of the code"""
        with open(file_path, 'r') as f:
            code = f.read()
            tree = ast.parse(code)
            
        # Calculate complexity metrics
        complexities = {}
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                complexity = self._calculate_complexity(node)
                complexities[node.name] = complexity
                
        # Generate heatmap
        plt.figure(figsize=(12, 8))
        names = list(complexities.keys())
        values = list(complexities.values())
        
        plt.bar(names, values, color='red')
        plt.xticks(rotation=45)
        plt.title('Code Complexity Heatmap')
        plt.ylabel('Complexity Score')
        
        if output_path:
            plt.savefig(output_path)
            plt.close()
            
        return {
            "complexities": complexities,
            "file": file_path,
            "output": output_path
        }
        
    def _calculate_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity"""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While,
                                ast.Try, ast.ExceptHandler)):
                complexity += 1
        return complexity 