from typing import Dict, List, Optional
from pathlib import Path
import ast
import re
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class SecurityAnalyzer:
    """Analyzes Python code for security vulnerabilities"""
    
    def __init__(self, config):
        self.config = config
        self.llm = ChatOpenAI(
            model_name=config.model,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            api_key=config.api_key
        )
        
        # Common security patterns to check
        self.vulnerability_patterns = {
            'sql_injection': [
                r'execute\(.*?\)',
                r'executemany\(.*?\)',
                r'cursor\.execute\(.*?\)',
                r'cursor\.executemany\(.*?\)'
            ],
            'command_injection': [
                r'os\.system\(.*?\)',
                r'subprocess\.run\(.*?\)',
                r'subprocess\.Popen\(.*?\)',
                r'os\.popen\(.*?\)'
            ],
            'path_traversal': [
                r'open\(.*?\)',
                r'file\(.*?\)',
                r'Path\(.*?\)'
            ],
            'hardcoded_secrets': [
                r'password\s*=\s*[\'"].*?[\'"]',
                r'api_key\s*=\s*[\'"].*?[\'"]',
                r'secret\s*=\s*[\'"].*?[\'"]',
                r'token\s*=\s*[\'"].*?[\'"]'
            ],
            'insecure_random': [
                r'random\.randint\(.*?\)',
                r'random\.choice\(.*?\)',
                r'random\.random\(\)'
            ]
        }
        
    def analyze_file(self, file_path: str) -> Dict:
        """Analyze a Python file for security vulnerabilities"""
        with open(file_path, 'r') as f:
            code = f.read()
            
        # Static analysis
        static_findings = self._static_analysis(code)
        
        # AI-powered analysis
        ai_findings = self._ai_analysis(code)
        
        # Combine results
        findings = {
            'static_analysis': static_findings,
            'ai_analysis': ai_findings,
            'file': file_path
        }
        
        return findings
        
    def _static_analysis(self, code: str) -> Dict:
        """Perform static analysis for known vulnerability patterns"""
        findings = {}
        
        for vuln_type, patterns in self.vulnerability_patterns.items():
            matches = []
            for pattern in patterns:
                for match in re.finditer(pattern, code):
                    matches.append({
                        'line': code[:match.start()].count('\n') + 1,
                        'code': match.group(),
                        'pattern': pattern
                    })
            if matches:
                findings[vuln_type] = matches
                
        return findings
        
    def _ai_analysis(self, code: str) -> Dict:
        """Perform AI-powered security analysis"""
        prompt = ChatPromptTemplate.from_template("""
        Analyze the following Python code for security vulnerabilities:
        
        Code:
        {code}
        
        Look for:
        1. Input validation issues
        2. Authentication and authorization problems
        3. Data protection concerns
        4. API security issues
        5. Cryptography weaknesses
        6. Error handling that might leak sensitive information
        
        Provide a detailed analysis with:
        1. Vulnerability descriptions
        2. Risk levels (High/Medium/Low)
        3. Code locations
        4. Recommended fixes
        """)
        
        chain = prompt | self.llm | StrOutputParser()
        analysis = chain.invoke({"code": code})
        
        return {
            'analysis': analysis
        }
        
    def generate_security_report(self, findings: Dict) -> str:
        """Generate a comprehensive security report"""
        report = []
        report.append("# Security Analysis Report\n")
        
        # Static analysis findings
        if findings['static_analysis']:
            report.append("## Static Analysis Findings\n")
            for vuln_type, matches in findings['static_analysis'].items():
                report.append(f"### {vuln_type.replace('_', ' ').title()}\n")
                for match in matches:
                    report.append(f"- Line {match['line']}: {match['code']}")
                    report.append(f"  Pattern: {match['pattern']}\n")
                    
        # AI analysis findings
        if findings['ai_analysis']:
            report.append("## AI-Powered Analysis\n")
            report.append(findings['ai_analysis']['analysis'])
            
        return '\n'.join(report)
        
    def suggest_fixes(self, file_path: str) -> Dict:
        """Suggest fixes for identified security issues"""
        findings = self.analyze_file(file_path)
        
        prompt = ChatPromptTemplate.from_template("""
        Suggest specific fixes for the following security issues:
        
        Findings:
        {findings}
        
        Provide:
        1. Code-level fixes
        2. Architecture-level recommendations
        3. Best practices to implement
        4. Security libraries to use
        5. Testing strategies
        """)
        
        chain = prompt | self.llm | StrOutputParser()
        fixes = chain.invoke({"findings": str(findings)})
        
        return {
            'findings': findings,
            'fixes': fixes
        } 