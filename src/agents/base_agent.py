"""
Base agent implementation for Amber.txt

Provides the foundation for specialized agents in the system.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import json
from datetime import datetime


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the Amber system.
    Defines the core functionality that all agents must implement.
    """
    
    def __init__(self, agent_id: str, name: str, description: str):
        """
        Initialize the base agent.
        
        Args:
            agent_id: Unique identifier for the agent
            name: Human-readable name for the agent
            description: Description of the agent's purpose
        """
        self.agent_id = agent_id
        self.name = name
        self.description = description
        
        # Track metadata about agent usage
        self.metadata = {
            "created_at": datetime.now().isoformat(),
            "last_active": None,
            "request_count": 0,
            "success_count": 0,
            "failure_count": 0
        }
    
    @abstractmethod
    def process(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a query with the agent and return a result.
        
        Args:
            query: The user query or task to process
            context: Additional context for the query (conversation history, etc)
            
        Returns:
            A dictionary containing the agent's response and metadata
        """
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        Return a list of capabilities this agent provides.
        
        Returns:
            List of capability strings that describe what the agent can do
        """
        pass
    
    def update_metadata(self, success: bool = True) -> None:
        """
        Update the agent's usage metadata.
        
        Args:
            success: Whether the agent's processing was successful
        """
        self.metadata["last_active"] = datetime.now().isoformat()
        self.metadata["request_count"] += 1
        
        if success:
            self.metadata["success_count"] += 1
        else:
            self.metadata["failure_count"] += 1
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get the agent's metadata.
        
        Returns:
            Dictionary containing agent metadata
        """
        return self.metadata
    
    def should_handle(self, query: str, context: Dict[str, Any]) -> float:
        """
        Determine if this agent should handle the given query and with what confidence.
        
        Args:
            query: The user query
            context: Additional context
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        # Default implementation always returns 0.0 (no confidence)
        # Subclasses should override this method
        return 0.0
    
    def __repr__(self) -> str:
        """
        String representation of the agent.
        """
        return f"{self.name} (ID: {self.agent_id})"