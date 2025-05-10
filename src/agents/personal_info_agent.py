"""
Personal Information Agent for Amber.txt

Manages and retrieves user details, preferences, and personal information.
"""
from typing import Dict, List, Any, Optional
import re

from .base_agent import BaseAgent
from ..memory.storage import MemoryStorage


class PersonalInfoAgent(BaseAgent):
    """
    Agent responsible for handling personal information about the user.
    Stores and retrieves preferences, details, and other personal data.
    """
    
    def __init__(self, memory_storage: MemoryStorage):
        """
        Initialize the personal info agent.
        
        Args:
            memory_storage: Memory storage instance to use
        """
        super().__init__(
            agent_id="personal_info",
            name="Personal Information Agent",
            description="Manages user personal information and preferences"
        )
        self.memory_storage = memory_storage
        self.personal_info_topic = "personal_info"
        
        # Common patterns for personal information requests
        self.patterns = {
            "preference": r"(prefer|like|favorite|enjoy|hate|dislike)",
            "personal": r"(my|I am|I'm|I was|I have|I've|my name|my age|my address|my email|my phone)",
            "fact": r"(fact about me|remember that I|recall that I|note that I)",
        }
    
    def get_capabilities(self) -> List[str]:
        """
        Return capabilities of the personal info agent.
        """
        return [
            "Store personal information about the user",
            "Retrieve user preferences",
            "Answer questions about user characteristics",
            "Recognize when personal information is being shared",
            "Maintain consistent user profile"
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
        confidence = 0.0
        
        # Check for personal info patterns
        for pattern_name, pattern in self.patterns.items():
            matches = re.findall(pattern, query.lower())
            if matches:
                confidence = max(confidence, 0.7)
        
        # Check for direct questions about preferences/info
        if "what do I like" in query.lower() or "what is my" in query.lower():
            confidence = max(confidence, 0.9)
            
        # Check if the query is asking to remember something personal
        if "remember" in query.lower() and any(p in query.lower() for p in ["i am", "i like", "i prefer", "my"]):
            confidence = max(confidence, 0.9)
            
        return confidence
    
    def process(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a query for personal information.
        
        Args:
            query: The user query
            context: Additional context (conversation history, etc)
            
        Returns:
            Response with personal information or confirmation of storage
        """
        self.update_metadata()
        
        # Determine if we need to store information or retrieve it
        if self._is_storage_request(query):
            return self._handle_storage(query, context)
        else:
            return self._handle_retrieval(query, context)
    
    def _is_storage_request(self, query: str) -> bool:
        """
        Determine if the query is asking to store information.
        """
        storage_indicators = [
            "remember that", 
            "make note that", 
            "keep in mind that",
            "don't forget that",
            "I want you to know that"
        ]
        
        return any(indicator in query.lower() for indicator in storage_indicators)
    
    def _handle_storage(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a request to store personal information.
        """
        # Extract the information to store
        info_match = re.search(r"(?:remember that|make note that|keep in mind that|don't forget that|I want you to know that)(.*)", query, re.IGNORECASE)
        
        if not info_match:
            return {
                "response": "I'm not sure what personal information you'd like me to remember. Could you phrase it differently?",
                "confidence": 0.5,
                "agent_id": self.agent_id
            }
        
        info_to_store = info_match.group(1).strip()
        
        # Generate tags based on the content
        tags = ["personal_info"]
        if any(word in info_to_store.lower() for word in ["like", "prefer", "favorite", "enjoy"]):
            tags.append("preference")
        if any(word in info_to_store.lower() for word in ["address", "email", "phone", "contact"]):
            tags.append("contact")
        if any(word in info_to_store.lower() for word in ["job", "work", "career", "profession"]):
            tags.append("career")
        
        # Store the information
        memory_id = self.memory_storage.add_memory(
            content=info_to_store,
            tags=tags,
            topic=self.personal_info_topic,
            importance=8,  # Personal info is generally important
            source="user_statement"
        )
        
        return {
            "response": f"I've remembered that {info_to_store}.",
            "confidence": 0.9,
            "agent_id": self.agent_id,
            "memory_id": memory_id
        }
    
    def _handle_retrieval(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a request to retrieve personal information.
        """
        # Determine what kind of information is being requested
        query_lower = query.lower()
        
        # Prepare search terms based on the query
        search_terms = []
        
        # Look for preference questions
        if any(word in query_lower for word in ["like", "prefer", "favorite", "enjoy"]):
            search_terms.append("like")
            search_terms.append("prefer")
            search_terms.append("favorite")
            search_terms.append("enjoy")
            
            # Extract what the preference is about, e.g., "food", "movie"
            preference_type_match = re.search(r"(?:like|prefer|favorite|enjoy)(?:\s+\w+){0,3}\s+(\w+)", query_lower)
            if preference_type_match:
                search_terms.append(preference_type_match.group(1))
        
        # Look for personal facts
        elif "what is my" in query_lower or "what's my" in query_lower:
            fact_match = re.search(r"what(?:'s| is) my (\w+)", query_lower)
            if fact_match:
                search_terms.append(fact_match.group(1))
        
        # Search memories with the constructed terms
        memories = []
        for term in search_terms:
            results = self.memory_storage.search_memories(
                query=term,
                topic=self.personal_info_topic,
                limit=5
            )
            memories.extend(results)
        
        # Remove duplicates
        unique_memories = []
        memory_ids = set()
        for memory in memories:
            if memory["id"] not in memory_ids:
                unique_memories.append(memory)
                memory_ids.add(memory["id"])
        
        if not unique_memories:
            return {
                "response": "I don't seem to have any information about that in my memory. Would you like to tell me?",
                "confidence": 0.6,
                "agent_id": self.agent_id
            }
        
        # Construct a response based on found memories
        response = "Based on what you've told me, "
        
        if len(unique_memories) == 1:
            response += unique_memories[0]["content"]
        else:
            response += "I know a few things about that: "
            for i, memory in enumerate(unique_memories):
                if i > 0:
                    response += "; "
                response += memory["content"]
        
        return {
            "response": response,
            "confidence": 0.8,
            "agent_id": self.agent_id,
            "memories_used": [m["id"] for m in unique_memories]
        }