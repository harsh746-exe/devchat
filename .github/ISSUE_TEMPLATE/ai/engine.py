"""
AI Engine for code assistance.
"""

import os
from typing import Optional, Dict, List, Any
import openai
from openai import OpenAI
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential

class AIEngine:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        """Initialize the AI engine with OpenAI credentials.
        
        Args:
            api_key: OpenAI API key
            model: Model to use for completions
        """
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        logger.info(f"AI Engine initialized with model: {model}")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def get_completion(self, 
                           messages: List[Dict[str, str]], 
                           temperature: float = 0.7,
                           max_tokens: Optional[int] = None) -> str:
        """Get a completion from the AI model.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Controls randomness in the response
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Generated text completion
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error getting completion: {str(e)}")
            raise

    async def analyze_code(self, code: str, context: Optional[str] = None) -> Dict[str, Any]:
        """Analyze code and provide suggestions.
        
        Args:
            code: Code to analyze
            context: Additional context about the code
            
        Returns:
            Dictionary containing analysis results
        """
        messages = [
            {"role": "system", "content": "You are a helpful code analyzer. Provide detailed analysis and suggestions."},
            {"role": "user", "content": f"Analyze this code:\n\n{code}\n\nContext: {context if context else 'No additional context provided.'}"}
        ]
        
        analysis = await self.get_completion(messages, temperature=0.3)
        return {
            "analysis": analysis,
            "suggestions": await self._extract_suggestions(analysis)
        }

    async def _extract_suggestions(self, analysis: str) -> List[str]:
        """Extract specific suggestions from the analysis.
        
        Args:
            analysis: Full analysis text
            
        Returns:
            List of specific suggestions
        """
        messages = [
            {"role": "system", "content": "Extract specific suggestions from the analysis."},
            {"role": "user", "content": f"Extract specific suggestions from this analysis:\n\n{analysis}"}
        ]
        
        suggestions = await self.get_completion(messages, temperature=0.2)
        return [s.strip() for s in suggestions.split('\n') if s.strip()]

    def generate_tests(self, code: str) -> str:
        """Generate unit tests for the given code."""
        prompt = f"""Generate comprehensive unit tests for this code:
```
{code}
```
Include test cases for:
1. Normal operation
2. Edge cases
3. Error conditions"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert in writing unit tests."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating tests: {str(e)}" 