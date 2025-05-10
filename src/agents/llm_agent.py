"""
LLM-powered Agent for Amber.txt

Base agent implementation that uses an LLM to process queries.
"""
from typing import Dict, List, Any, Optional
import json

from .base_agent import BaseAgent
from ..utils.llm import LLMInterface
from ..memory.storage import MemoryStorage


class LLMAgent(BaseAgent):
    """
    Agent that uses an LLM to process queries.
    Can be extended by specialized agents that need LLM capabilities.
    """
    
    def __init__(self, 
                 agent_id: str,
                 name: str,
                 description: str,
                 llm_interface: LLMInterface,
                 memory_storage: Optional[MemoryStorage] = None,
                 system_prompt: Optional[str] = None):
        """
        Initialize the LLM agent.
        
        Args:
            agent_id: Unique identifier for the agent
            name: Human-readable name for the agent
            description: Description of the agent's purpose
            llm_interface: LLM interface to use for processing
            memory_storage: Optional memory storage instance
            system_prompt: System prompt to use for the LLM
        """
        super().__init__(agent_id, name, description)
        self.llm = llm_interface
        self.memory_storage = memory_storage
        self.system_prompt = system_prompt or self._get_default_system_prompt()
        
    def process(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a query with the LLM and return a result.
        
        Args:
            query: The user query or task to process
            context: Additional context for the query (conversation history, etc)
            
        Returns:
            A dictionary containing the agent's response and metadata
        """
        self.update_metadata()
        
        # Prepare messages for the LLM
        messages = self._prepare_messages(query, context)
        
        # Generate a response from the LLM
        llm_response = self.llm.generate_response(
            messages=messages,
            system_prompt=self.system_prompt
        )
        
        # Process the LLM response
        processed_response = self._process_llm_response(llm_response, query, context)
        
        # Add agent metadata to the response
        processed_response.update({
            "agent_id": self.agent_id,
            "confidence": 0.7,  # Default confidence
        })
        
        return processed_response
    
    def _prepare_messages(self, query: str, context: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Prepare messages for the LLM based on query and context.
        
        Args:
            query: The user query
            context: Additional context
            
        Returns:
            List of messages to send to the LLM
        """
        messages = []
        
        # Add conversation history if available
        if "conversation_history" in context:
            # Limit to last few messages to avoid context window issues
            for message in context["conversation_history"][-5:]:
                messages.append({
                    "role": message["role"],
                    "content": message["content"]
                })
        
        # Add the current user query if it's not already included
        if not messages or messages[-1]["role"] != "user" or messages[-1]["content"] != query:
            messages.append({
                "role": "user",
                "content": query
            })
        
        return messages
    
    def _process_llm_response(self, 
                              llm_response: Dict[str, Any], 
                              query: str, 
                              context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the raw LLM response.
        
        Args:
            llm_response: Response from the LLM
            query: The original user query
            context: The context provided for the query
            
        Returns:
            Processed response dictionary
        """
        # Extract the content from the LLM response
        content = llm_response.get("content", "")
        
        # If there was an error, handle it
        if "error" in llm_response:
            return {
                "response": "I'm having trouble accessing my language model. Please try again later.",
                "error": llm_response["error"]
            }
        
        # Return the processed response
        return {
            "response": content,
            "llm_model": llm_response.get("model", ""),
            "usage": llm_response.get("usage", {})
        }
    
    def get_capabilities(self) -> List[str]:
        """
        Return capabilities of the LLM agent.
        """
        return [
            "Answer general questions",
            "Engage in natural conversation",
            "Provide explanations and context"
        ]
    
    def should_handle(self, query: str, context: Dict[str, Any]) -> float:
        """
        Determine if this agent should handle the query.
        
        Args:
            query: The user query
            context: Additional context
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        # Base LLM agent is a general-purpose agent
        # It should handle queries that don't match other specialized agents
        return 0.5  # Medium confidence as fallback
    
    def _get_default_system_prompt(self) -> str:
        """
        Get the default system prompt for the LLM.
        
        Returns:
            Default system prompt
        """
        return f"""
        You are {self.name}, part of the Amber.txt personal AI assistant system.
        
        {self.description}
        
        Your role is to provide helpful, accurate, and friendly responses to the user.
        
        When responding:
        - Be concise and direct
        - Maintain a friendly and helpful tone
        - Use the user's conversation history for context
        - Be honest about limitations or uncertainty
        
        Respond in a natural, conversational manner.
        """