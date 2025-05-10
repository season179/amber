"""
Test script for the MemoryStorage class
"""
from src.memory.storage import MemoryStorage

def test_memory_operations():
    """Test basic memory operations"""
    import os
    from pathlib import Path

    # Use a dedicated test directory for memory tests
    tests_data_dir = Path(__file__).parent.parent / "data"
    if not tests_data_dir.exists():
        tests_data_dir.mkdir()

    test_dir = str(tests_data_dir / "memory_test_store")
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    # Initialize memory storage with the test directory
    memory = MemoryStorage(storage_dir=test_dir, format_type="json")
    
    # Add a test memory
    test_content = "This is a test memory"
    memory_id = memory.add_memory(
        content=test_content,
        tags=["test"],
        importance=5,
        source="test_script"
    )
    
    print(f"Added memory with ID: {memory_id}")
    
    # Retrieve the memory
    retrieved = memory.get_memory(memory_id)
    
    if retrieved:
        print(f"Retrieved memory: {retrieved['content']}")
        print(f"Memory tags: {retrieved['tags']}")
        print(f"Access count: {retrieved['access_count']}")
    else:
        print("Failed to retrieve memory!")
    
    # Search for memories
    search_results = memory.search_memories(query="test")
    print(f"Search found {len(search_results)} results")
    
    # Update the memory
    update_success = memory.update_memory(
        memory_id=memory_id,
        content="Updated test memory",
        importance=8
    )
    
    print(f"Memory update success: {update_success}")
    
    # Retrieve the updated memory
    updated = memory.get_memory(memory_id)
    if updated:
        print(f"Updated memory: {updated['content']}")
        print(f"Updated importance: {updated['importance']}")
    
    print("Memory test completed!")

if __name__ == "__main__":
    test_memory_operations()