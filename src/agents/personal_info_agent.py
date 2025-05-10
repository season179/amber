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
        query_lower = query.lower()

        # Check for storage requests first
        if self._is_storage_request(query):
            # Check if it's personal information
            if any(p in query_lower for p in ["i am", "i like", "i prefer", "my", "i live", "i work",
                                             "i have", "i've", "i don't", "allergic", "allergy"]):
                return 0.95  # Very high confidence for storing personal info

        # Check for personal info patterns
        for pattern_name, pattern in self.patterns.items():
            matches = re.findall(pattern, query_lower)
            if matches:
                confidence = max(confidence, 0.7)

        # Check for direct questions about preferences/info
        if any(q in query_lower for q in ["what do i like", "what is my", "what's my", "where do i",
                                         "where i live", "where i work", "what allergies",
                                         "am i allergic", "when is my", "how old"]):
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
        query_lower = query.lower()

        # Direct storage indicators
        storage_indicators = [
            "remember that",
            "remember when",
            "remember my",
            "make note that",
            "make a note",
            "keep in mind that",
            "don't forget that",
            "i want you to know that",
            "i want you to remember",
            "i should tell you that",
            "i should mention that",
            "just so you know"
        ]

        # Check for direct indicators
        if any(indicator in query_lower for indicator in storage_indicators):
            return True

        # Check for expressions with "please" followed by remember/note
        please_patterns = [
            "please remember",
            "please note",
            "could you remember",
            "can you remember",
            "would you remember"
        ]

        if any(pattern in query_lower for pattern in please_patterns):
            return True

        # Check for sentences starting with "I am", "I have", etc. that suggest sharing personal info
        first_words = query_lower.split()[:3]
        first_phrase = " ".join(first_words)

        statement_starts = [
            "i am ", "i'm ",
            "i have ", "i've ",
            "i like ", "i prefer ",
            "i live ", "i work ",
            "i don't ", "i do not ",
            "my name ", "my address ",
            "my birthday ", "my favorite "
        ]

        for start in statement_starts:
            if query_lower.startswith(start):
                return True

        return False
    
    def _handle_storage(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a request to store personal information.
        """
        query_lower = query.lower()

        # Try to extract information to store with different patterns
        info_to_store = None

        # Pattern 1: Classic "remember that..." pattern
        standard_patterns = [
            r"(?:remember that|make note that|keep in mind that|don't forget that|I want you to know that|just so you know that|I should tell you that|I should mention that)(.*)",
            r"(?:remember when|remember my|make a note of my|make a note about)(.*)"
        ]

        for pattern in standard_patterns:
            info_match = re.search(pattern, query, re.IGNORECASE)
            if info_match:
                info_to_store = info_match.group(1).strip()
                break

        # Pattern 2: Direct statements starting with I am, I have, etc.
        if not info_to_store and any(query_lower.startswith(start) for start in [
            "i am", "i'm", "i have", "i've", "i like", "i prefer",
            "i live", "i work", "i don't", "i do not", "my name", "my address"
        ]):
            info_to_store = query.strip()

        # Pattern 3: If we can't extract it, use the whole query as a fallback
        if not info_to_store and self._is_storage_request(query):
            # Remove prefixes like "Please remember" if present
            for prefix in ["please", "can you", "could you"]:
                if query_lower.startswith(prefix):
                    query = query[len(prefix):].strip()
            info_to_store = query.strip()

        if not info_to_store:
            return {
                "response": "I'm not sure what personal information you'd like me to remember. Could you phrase it differently?",
                "confidence": 0.5,
                "agent_id": self.agent_id
            }

        # Generate tags based on the content
        tags = ["personal_info"]
        info_lower = info_to_store.lower()

        # Preference tags
        if any(word in info_lower for word in ["like", "prefer", "favorite", "enjoy", "love"]):
            tags.append("preference")

        # Contact tags
        if any(word in info_lower for word in ["address", "email", "phone", "contact", "number", "live in", "live at"]):
            tags.append("contact")

        # Work tags
        if any(word in info_lower for word in ["job", "work", "career", "profession", "company", "business"]):
            tags.append("career")

        # Health tags
        if any(word in info_lower for word in ["allerg", "health", "condition", "disease", "medication", "medicine"]):
            tags.append("health")

        # Relationship tags
        if any(word in info_lower for word in ["family", "child", "parent", "mother", "father", "sibling", "married", "spouse"]):
            tags.append("relationship")

        # Store the information
        memory_id = self.memory_storage.add_memory(
            content=info_to_store,
            tags=tags,
            topic=self.personal_info_topic,
            importance=8,  # Personal info is generally important
            source="user_statement"
        )

        # Construct a natural-sounding confirmation response
        if "remember that" in query_lower or info_to_store.lower().startswith("i "):
            response = f"I've remembered that {info_to_store}."
        else:
            response = f"I've made a note about {info_to_store}."

        return {
            "response": response,
            "confidence": 0.95,
            "agent_id": self.agent_id,
            "memory_id": memory_id
        }
    
    def _handle_retrieval(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a request to retrieve personal information.
        """
        # Determine what kind of information is being requested
        query_lower = query.lower()

        # Prepare search terms and tags based on the query
        search_terms = []
        search_tags = []

        # Look for preference questions
        if any(word in query_lower for word in ["like", "prefer", "favorite", "enjoy", "love"]):
            search_terms.extend(["like", "prefer", "favorite", "enjoy", "love"])
            search_tags.append("preference")

            # Extract what the preference is about, e.g., "food", "movie"
            preference_objects = ["food", "movie", "book", "music", "color", "sport", "hobby",
                                 "drink", "place", "restaurant", "animal", "tv", "show", "game",
                                 "ice cream", "fruit", "vegetable"]

            for obj in preference_objects:
                if obj in query_lower:
                    search_terms.append(obj)

        # Look for location information
        elif any(term in query_lower for term in ["where do i live", "where i live", "my address", "my location", "my home"]):
            search_terms.extend(["live", "address", "home", "location", "city", "street"])
            search_tags.append("contact")

        # Look for work information
        elif any(term in query_lower for term in ["where do i work", "my job", "my career", "my company"]):
            search_terms.extend(["work", "job", "career", "company", "business", "profession"])
            search_tags.append("career")

        # Look for health information
        elif any(term in query_lower for term in ["allerg", "health", "condition", "medical"]):
            search_terms.extend(["allergic", "allergy", "health", "condition", "medication"])
            search_tags.append("health")

        # Look for personal facts
        elif "what is my" in query_lower or "what's my" in query_lower:
            fact_match = re.search(r"what(?:'s| is) my (\w+)", query_lower)
            if fact_match:
                search_terms.append(fact_match.group(1))

        # If we couldn't identify specific terms, extract key nouns
        if not search_terms:
            # Extract nouns (simplistic approach)
            words = query_lower.split()
            for word in words:
                if len(word) > 3 and word not in ["what", "where", "when", "which", "about", "with", "that", "this"]:
                    search_terms.append(word)

        # Make sure we have at least some search terms
        if not search_terms:
            search_terms = ["I", "my", "me"]  # Generic fallback terms

        # Search memories with the constructed terms
        memories = []

        # First try searching with tags if available
        if search_tags:
            for tag in search_tags:
                results = self.memory_storage.search_memories(
                    topic=self.personal_info_topic,
                    tags=[tag],
                    limit=5
                )
                memories.extend(results)

        # Then try searching with terms
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
            "confidence": 0.9,
            "agent_id": self.agent_id,
            "memories_used": [m["id"] for m in unique_memories]
        }