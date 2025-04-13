"""
Workflow management system.
"""

import os
import yaml
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path
from loguru import logger

from devchat.ai.engine import AIEngine
from devchat.analyzer.code_analyzer import CodeAnalyzer

class WorkflowManager:
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the workflow manager.
        
        Args:
            config_path: Path to workflow configuration file
        """
        self.config_path = config_path or str(Path.home() / ".devchat" / "workflows.yaml")
        self.workflows: Dict[str, Dict[str, Any]] = {}
        self._load_workflows()

    def _load_workflows(self):
        """Load workflows from configuration file."""
        try:
            config_path = Path(self.config_path)
            if config_path.exists():
                with open(config_path, 'r') as f:
                    self.workflows = yaml.safe_load(f) or {}
            logger.info(f"Loaded {len(self.workflows)} workflows from {self.config_path}")
        except Exception as e:
            logger.error(f"Error loading workflows: {str(e)}")
            self.workflows = {}

    def _save_workflows(self):
        """Save workflows to configuration file."""
        try:
            config_path = Path(self.config_path)
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, 'w') as f:
                yaml.dump(self.workflows, f)
            logger.info(f"Saved {len(self.workflows)} workflows to {self.config_path}")
        except Exception as e:
            logger.error(f"Error saving workflows: {str(e)}")

    def add_workflow(self, name: str, workflow: Dict[str, Any]):
        """Add a new workflow.
        
        Args:
            name: Name of the workflow
            workflow: Workflow configuration
        """
        self.workflows[name] = workflow
        self._save_workflows()
        logger.info(f"Added workflow: {name}")

    def remove_workflow(self, name: str):
        """Remove a workflow.
        
        Args:
            name: Name of the workflow to remove
        """
        if name in self.workflows:
            del self.workflows[name]
            self._save_workflows()
            logger.info(f"Removed workflow: {name}")

    def get_workflow(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a workflow by name.
        
        Args:
            name: Name of the workflow
            
        Returns:
            Workflow configuration if found, None otherwise
        """
        return self.workflows.get(name)

    def list_workflows(self) -> List[str]:
        """List all available workflows.
        
        Returns:
            List of workflow names
        """
        return list(self.workflows.keys())

    def execute_workflow(self, name: str, **kwargs) -> Dict[str, Any]:
        """Execute a workflow.
        
        Args:
            name: Name of the workflow to execute
            **kwargs: Additional arguments for the workflow
            
        Returns:
            Results of the workflow execution
        """
        workflow = self.get_workflow(name)
        if not workflow:
            raise ValueError(f"Workflow '{name}' not found")

        try:
            # Execute workflow steps
            results = {}
            for step in workflow.get('steps', []):
                step_type = step.get('type')
                if step_type == 'code_analysis':
                    results['analysis'] = self._execute_code_analysis(step, **kwargs)
                elif step_type == 'test_generation':
                    results['tests'] = self._execute_test_generation(step, **kwargs)
                elif step_type == 'refactoring':
                    results['refactoring'] = self._execute_refactoring(step, **kwargs)
            
            return results
        except Exception as e:
            logger.error(f"Error executing workflow {name}: {str(e)}")
            raise

    def _execute_code_analysis(self, step: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Execute code analysis step."""
        # Implementation for code analysis
        pass

    def _execute_test_generation(self, step: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Execute test generation step."""
        # Implementation for test generation
        pass

    def _execute_refactoring(self, step: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Execute code refactoring step."""
        # Implementation for refactoring
        pass

    def create_workflow(self, name: str, description: str = "", steps: List[Dict] = None) -> bool:
        """Create a new workflow."""
        workflow_path = os.path.join(self.workflows_dir, f"{name}.yml")
        
        if os.path.exists(workflow_path):
            return False
        
        workflow = {
            "name": name,
            "description": description,
            "steps": steps or [],
            "created_at": str(datetime.now()),
            "modified_at": str(datetime.now())
        }
        
        with open(workflow_path, 'w') as f:
            yaml.dump(workflow, f)
        
        return True

    def update_workflow(self, name: str, updates: Dict) -> bool:
        """Update an existing workflow."""
        workflow = self.get_workflow(name)
        if not workflow:
            return False
        
        workflow.update(updates)
        workflow["modified_at"] = str(datetime.now())
        
        path = os.path.join(self.workflows_dir, f"{name}.yml")
        with open(path, 'w') as f:
            yaml.dump(workflow, f)
        
        return True

    def delete_workflow(self, name: str) -> bool:
        """Delete a workflow."""
        path = os.path.join(self.workflows_dir, f"{name}.yml")
        if not os.path.exists(path):
            return False
        
        os.remove(path)
        return True

    def run_workflow(self, name: str, context: Dict = None) -> Dict:
        """Run a workflow with optional context."""
        workflow = self.get_workflow(name)
        if not workflow:
            return {"success": False, "error": "Workflow not found"}
        
        results = []
        context = context or {}
        
        try:
            for step in workflow.get("steps", []):
                step_type = step.get("type")
                step_config = step.get("config", {})
                
                if step_type == "analyze":
                    # Run code analysis
                    file = step_config.get("file")
                    if file and os.path.exists(file):
                        analyzer = CodeAnalyzer()
                        analysis = analyzer.analyze_complexity(file)
                        results.append({
                            "step": "analyze",
                            "results": analysis
                        })
                
                elif step_type == "assist":
                    # Get AI assistance
                    query = step_config.get("query")
                    if query:
                        ai_engine = AIEngine()
                        response = ai_engine.get_code_assistance(query, context.get("code"))
                        results.append({
                            "step": "assist",
                            "results": response
                        })
                
                elif step_type == "test":
                    # Generate tests
                    file = step_config.get("file")
                    if file and os.path.exists(file):
                        ai_engine = AIEngine()
                        tests = ai_engine.generate_tests(file)
                        results.append({
                            "step": "test",
                            "results": tests
                        })
            
            return {
                "success": True,
                "workflow": name,
                "results": results
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "partial_results": results
            } 