from typing import Dict, List, Optional
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import os

class CodeAssistant:
    """AI-powered code assistant"""
    
    def __init__(self, config):
        self.config = config
        self.memory = ConversationBufferMemory()
        self.llm = ChatOpenAI(
            model_name=config.model,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            api_key=config.api_key
        )
        
    def analyze_code(self, file_path: str) -> Dict:
        """Analyze code and provide AI-powered suggestions"""
        with open(file_path, 'r') as f:
            code = f.read()
            
        prompt = ChatPromptTemplate.from_template("""
        Analyze the following Python code and provide detailed suggestions for improvement:
        Focus on:
        1. Code quality and best practices
        2. Performance optimizations
        3. Security considerations
        4. Maintainability
        5. Documentation
        
        Code:
        {code}
        
        Provide your analysis in a structured format with specific examples and recommendations.
        """)
        
        chain = prompt | self.llm | StrOutputParser()
        analysis = chain.invoke({"code": code})
        
        return {
            "analysis": analysis,
            "file": file_path
        }
        
    def answer_question(self, question: str) -> str:
        """Answer coding-related questions"""
        prompt = ChatPromptTemplate.from_template("""
        You are an expert Python developer. Answer the following question with detailed explanations and code examples when appropriate:
        
        Question: {question}
        
        Provide a comprehensive answer that includes:
        1. Clear explanation of the concept
        2. Code examples if applicable
        3. Best practices and common pitfalls
        4. Additional resources for learning more
        """)
        
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({"question": question})
        
    def refactor_code(self, file_path: str, instructions: str) -> Dict:
        """Refactor code based on instructions"""
        with open(file_path, 'r') as f:
            code = f.read()
            
        prompt = ChatPromptTemplate.from_template("""
        Refactor the following Python code according to these instructions:
        {instructions}
        
        Original code:
        {code}
        
        Provide the refactored code with explanations of the changes made.
        Focus on:
        1. Code readability
        2. Performance improvements
        3. Best practices
        4. Maintainability
        """)
        
        chain = prompt | self.llm | StrOutputParser()
        refactored = chain.invoke({"instructions": instructions, "code": code})
        
        return {
            "original": code,
            "refactored": refactored,
            "file": file_path
        }
        
    def generate_documentation(self, file_path: str) -> Dict:
        """Generate documentation for code"""
        with open(file_path, 'r') as f:
            code = f.read()
            
        prompt = ChatPromptTemplate.from_template("""
        Generate comprehensive documentation for the following Python code:
        
        Code:
        {code}
        
        Include:
        1. Module/package description
        2. Function/class documentation
        3. Usage examples
        4. Parameters and return values
        5. Exceptions and error handling
        """)
        
        chain = prompt | self.llm | StrOutputParser()
        documentation = chain.invoke({"code": code})
        
        return {
            "documentation": documentation,
            "file": file_path
        }
        
    def chat(self, message: str) -> str:
        """Have a conversation about code"""
        conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            verbose=True
        )
        return conversation.predict(input=message) 