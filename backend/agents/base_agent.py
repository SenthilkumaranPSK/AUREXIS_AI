"""
Base Agent
Abstract base class for all specialized agents
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime


class BaseAgent(ABC):
    """Base class for all financial agents"""
    
    def __init__(self, name: str, role: str, capabilities: List[str]):
        self.name = name
        self.role = role
        self.capabilities = capabilities
        self.status = "ready"
        self.last_execution = None
        self.execution_count = 0
    
    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute agent task
        
        Args:
            task: Dictionary containing task details and data
            
        Returns:
            Dictionary containing execution results
        """
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "name": self.name,
            "role": self.role,
            "capabilities": self.capabilities,
            "status": self.status,
            "last_execution": self.last_execution,
            "execution_count": self.execution_count
        }
    
    def _update_status(self, status: str):
        """Update agent status"""
        self.status = status
        if status == "completed":
            self.last_execution = datetime.now().isoformat()
            self.execution_count += 1
    
    def can_handle(self, task_type: str) -> bool:
        """Check if agent can handle a task type"""
        return task_type in self.capabilities
