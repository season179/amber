"""
Dispatcher Agent for Amber.txt

Coordinates other agents and determines which agent should handle a query.
"""
from typing import Dict, List, Any, Optional
import re

from .base_agent import BaseAgent


class DispatcherAgent:
    """
    Dispatches queries to the appropriate specialized agent(s).
    Acts as the central coordinator for the agent system.
    """
    
    def __init__(self):
        """
        Initialize the dispatcher agent.
        """
        self.agents = {}  # Map of agent_id to agent instance
        self.fallback_agent_id = None
    
    def register_agent(self, agent: BaseAgent, is_fallback: bool = False) -> None:
        """
        Register an agent with the dispatcher.
        
        Args:
            agent: Agent instance to register
            is_fallback: Whether this agent should be used as fallback
        """
        self.agents[agent.agent_id] = agent
        
        if is_fallback:
            self.fallback_agent_id = agent.agent_id
    
    def dispatch(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Dispatch a query to the appropriate agent(s).
        
        Args:
            query: The user query
            context: Additional context like conversation history
            
        Returns:
            Response from the selected agent
        """
        # Score confidence for each agent
        confidence_scores = {}
        for agent_id, agent in self.agents.items():
            confidence_scores[agent_id] = agent.should_handle(query, context)
        
        # Find the agent with the highest confidence
        selected_agent_id = max(confidence_scores, key=confidence_scores.get)
        highest_confidence = confidence_scores[selected_agent_id]
        
        # Use fallback if no agent has sufficient confidence
        if highest_confidence < 0.5 and self.fallback_agent_id:
            selected_agent_id = self.fallback_agent_id
        
        # Process the query with the selected agent
        selected_agent = self.agents[selected_agent_id]
        result = selected_agent.process(query, context)
        
        # Add dispatcher metadata
        result["selected_by"] = "dispatcher"
        result["confidence_scores"] = confidence_scores
        
        return result
    
    def get_all_capabilities(self) -> Dict[str, List[str]]:
        """
        Get capabilities of all registered agents.
        
        Returns:
            Dictionary mapping agent IDs to their capabilities
        """
        capabilities = {}
        for agent_id, agent in self.agents.items():
            capabilities[agent_id] = agent.get_capabilities()
            
        return capabilities