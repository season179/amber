"""
Memory storage module for Amber.txt

Handles storage and retrieval of memories in a plain text format.
"""
import os
import json
import yaml
from datetime import datetime
from typing import Dict, List, Any, Optional, Union


class MemoryStorage:
    """
    Manages the storage and retrieval of memories in plain text format.
    Uses JSON/YAML for structured storage.
    """
    
    def __init__(self, storage_dir: str = "memory_store", 
                 format_type: str = "json"):
        """
        Initialize the memory storage system.
        
        Args:
            storage_dir: Directory to store memory files
            format_type: Format to store memories ('json' or 'yaml')
        """
        self.storage_dir = storage_dir
        self.format_type = format_type.lower()
        
        # Create storage directory if it doesn't exist
        os.makedirs(storage_dir, exist_ok=True)
        
        # Initialize general memories file
        self.general_file = os.path.join(storage_dir, f"general.{self.format_type}")
        self._initialize_file(self.general_file)
        
        # Initialize topic-based memory files
        self.topics = {}
        
    def _initialize_file(self, filepath: str) -> None:
        """Initialize a memory file if it doesn't exist."""
        if not os.path.exists(filepath):
            initial_data = {
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                    "version": "0.1"
                },
                "memories": []
            }
            
            self._write_to_file(filepath, initial_data)
    
    def _read_from_file(self, filepath: str) -> Dict[str, Any]:
        """Read and parse data from a memory file."""
        if not os.path.exists(filepath):
            return {"metadata": {}, "memories": []}
        
        with open(filepath, 'r') as f:
            if self.format_type == 'json':
                return json.load(f)
            elif self.format_type == 'yaml':
                return yaml.safe_load(f)
        
    def _write_to_file(self, filepath: str, data: Dict[str, Any]) -> None:
        """Write data to a memory file."""
        data["metadata"]["updated_at"] = datetime.now().isoformat()
        
        with open(filepath, 'w') as f:
            if self.format_type == 'json':
                json.dump(data, f, indent=2)
            elif self.format_type == 'yaml':
                yaml.dump(data, f)
    
    def add_memory(self, content: str,
                   tags: List[str] = None,
                   topic: str = None,
                   importance: int = 1,
                   source: str = "conversation") -> str:
        """
        Add a new memory to storage.

        Args:
            content: The memory content
            tags: List of tags to categorize the memory
            topic: Topic to store the memory under
            importance: Importance score (1-10)
            source: Source of the memory

        Returns:
            memory_id: ID of the created memory
        """
        if tags is None:
            tags = []

        # Generate a unique ID using timestamp and microseconds + random suffix
        timestamp = datetime.now()
        random_suffix = os.urandom(2).hex()  # 4 random hex characters
        memory_id = f"mem_{timestamp.strftime('%Y%m%d%H%M%S')}_{timestamp.microsecond}_{random_suffix}"

        memory = {
            "id": memory_id,
            "content": content,
            "created_at": timestamp.isoformat(),
            "last_accessed": timestamp.isoformat(),
            "access_count": 0,
            "importance": importance,
            "tags": tags,
            "source": source,
        }
        
        # Add to topic-specific file if topic is provided
        if topic:
            topic_file = os.path.join(self.storage_dir, f"topic_{topic}.{self.format_type}")
            self._initialize_file(topic_file)
            
            topic_data = self._read_from_file(topic_file)
            topic_data["memories"].append(memory)
            self._write_to_file(topic_file, topic_data)
            
            # Update topics index
            self.topics[topic] = topic_file
        
        # Also add to general file
        general_data = self._read_from_file(self.general_file)
        general_data["memories"].append(memory)
        self._write_to_file(self.general_file, general_data)
        
        return memory_id
    
    def get_memory(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific memory by ID.
        
        Args:
            memory_id: ID of the memory to retrieve
            
        Returns:
            Memory object or None if not found
        """
        general_data = self._read_from_file(self.general_file)
        
        for memory in general_data["memories"]:
            if memory["id"] == memory_id:
                # Update access metadata
                memory["last_accessed"] = datetime.now().isoformat()
                memory["access_count"] += 1
                self._write_to_file(self.general_file, general_data)
                return memory
        
        return None
    
    def search_memories(self,
                        query: str = None,
                        tags: List[str] = None,
                        topic: str = None,
                        limit: int = 10,
                        min_importance: int = 0) -> List[Dict[str, Any]]:
        """
        Search for memories based on criteria.

        Args:
            query: Text to search for in memory content
            tags: List of tags to filter by
            topic: Topic to search within
            limit: Maximum number of results
            min_importance: Minimum importance score

        Returns:
            List of matching memories
        """
        # Determine which file to search
        if topic:
            # If topic is provided but not in self.topics, check if the file exists
            topic_file = os.path.join(self.storage_dir, f"topic_{topic}.{self.format_type}")
            if os.path.exists(topic_file):
                # Add to topics dict if it exists but wasn't loaded
                self.topics[topic] = topic_file
                data = self._read_from_file(topic_file)
            elif topic in self.topics:
                data = self._read_from_file(self.topics[topic])
            else:
                # If topic doesn't exist, return empty results
                return []
        else:
            data = self._read_from_file(self.general_file)

        results = []

        for memory in data["memories"]:
            # Skip if below minimum importance
            if memory["importance"] < min_importance:
                continue

            # Filter by query text
            if query and query.lower() not in memory["content"].lower():
                continue

            # Filter by tags
            if tags:
                if not all(tag in memory["tags"] for tag in tags):
                    continue

            results.append(memory)

            # Update access metadata
            memory["last_accessed"] = datetime.now().isoformat()
            memory["access_count"] += 1

            if len(results) >= limit:
                break

        # Only write back if we found any results to update
        if results and topic:
            if topic in self.topics:
                self._write_to_file(self.topics[topic], data)
        elif results:
            self._write_to_file(self.general_file, data)

        return results
    
    def update_memory(self, memory_id: str, 
                      content: str = None,
                      tags: List[str] = None,
                      importance: int = None) -> bool:
        """
        Update an existing memory.
        
        Args:
            memory_id: ID of the memory to update
            content: New content (if updating)
            tags: New tags (if updating)
            importance: New importance score (if updating)
            
        Returns:
            True if successfully updated, False otherwise
        """
        general_data = self._read_from_file(self.general_file)
        
        for memory in general_data["memories"]:
            if memory["id"] == memory_id:
                if content is not None:
                    memory["content"] = content
                if tags is not None:
                    memory["tags"] = tags
                if importance is not None:
                    memory["importance"] = importance
                
                memory["last_accessed"] = datetime.now().isoformat()
                memory["access_count"] += 1
                
                self._write_to_file(self.general_file, general_data)
                return True
        
        return False
    
    def delete_memory(self, memory_id: str) -> bool:
        """
        Delete a memory.
        
        Args:
            memory_id: ID of the memory to delete
            
        Returns:
            True if successfully deleted, False otherwise
        """
        general_data = self._read_from_file(self.general_file)
        
        for i, memory in enumerate(general_data["memories"]):
            if memory["id"] == memory_id:
                general_data["memories"].pop(i)
                self._write_to_file(self.general_file, general_data)
                
                # Also remove from any topic files
                for topic_file in self.topics.values():
                    topic_data = self._read_from_file(topic_file)
                    for j, topic_memory in enumerate(topic_data["memories"]):
                        if topic_memory["id"] == memory_id:
                            topic_data["memories"].pop(j)
                            self._write_to_file(topic_file, topic_data)
                            break
                
                return True
                
        return False