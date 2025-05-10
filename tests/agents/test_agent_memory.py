"""
Test script for agent interaction with memory storage
"""
from src.memory.storage import MemoryStorage
from src.agents.personal_info_agent import PersonalInfoAgent

def test_personal_info_agent():
    """Test the PersonalInfoAgent's interaction with memory"""
    import os
    from pathlib import Path

    # Use a dedicated test directory for agent tests
    tests_data_dir = Path(__file__).parent.parent / "data"
    if not tests_data_dir.exists():
        tests_data_dir.mkdir()

    test_dir = str(tests_data_dir / "agent_test_store")
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    # Initialize memory storage with the test directory
    memory = MemoryStorage(storage_dir=test_dir, format_type="json")
    
    # Create personal info agent
    agent = PersonalInfoAgent(memory)
    
    # Test storing information
    store_query = "Remember that I like chocolate ice cream"
    context = {"conversation_history": []}
    
    print("Testing storage request:")
    result = agent.process(store_query, context)
    print(f"Response: {result['response']}")
    print(f"Memory ID: {result.get('memory_id', 'None')}")
    print(f"Confidence: {result.get('confidence', 0)}")
    
    # Test retrieving information
    retrieve_query = "What do I like to eat?"
    
    print("\nTesting retrieval request:")
    result = agent.process(retrieve_query, context)
    print(f"Response: {result['response']}")
    print(f"Memories used: {result.get('memories_used', [])}")
    print(f"Confidence: {result.get('confidence', 0)}")
    
    print("\nAgent memory test completed!")

if __name__ == "__main__":
    test_personal_info_agent()