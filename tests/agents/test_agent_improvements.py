"""
Test the improved PersonalInfoAgent with various query formats
"""
from src.memory.storage import MemoryStorage
from src.agents.personal_info_agent import PersonalInfoAgent

def test_agent_with_queries():
    """Test the agent with different query formats"""
    import os
    from pathlib import Path

    # Use a dedicated test directory for agent tests
    tests_data_dir = Path(__file__).parent.parent / "data"
    if not tests_data_dir.exists():
        tests_data_dir.mkdir()

    test_dir = str(tests_data_dir / "agent_improvements_store")
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    # Initialize memory storage with the test directory
    memory = MemoryStorage(storage_dir=test_dir, format_type="json")
    
    # Create personal info agent
    agent = PersonalInfoAgent(memory)
    
    # Test different storage request formats
    storage_queries = [
        "Remember that I live in San Francisco",
        "I live in San Francisco",
        "My address is 123 Main St",
        "I'm allergic to peanuts",
        "Please remember I work at Acme Corporation",
        "Just so you know I have a cat named Whiskers",
        "My birthday is April 15"
    ]
    
    print("TESTING STORAGE REQUESTS:")
    print("-" * 50)
    for query in storage_queries:
        print(f"\nQuery: '{query}'")
        print(f"Should handle confidence: {agent.should_handle(query, {})}")
        print(f"Is storage request: {agent._is_storage_request(query)}")
        
        result = agent.process(query, {})
        print(f"Response: {result['response']}")
        print(f"Memory ID: {result.get('memory_id', 'None')}")
        
    # Let's test retrieval with various formats
    retrieval_queries = [
        "Where do I live?",
        "What's my address?",
        "What allergies do I have?",
        "Where do I work?",
        "What's the name of my pet?",
        "When is my birthday?"
    ]
    
    print("\n\nTESTING RETRIEVAL REQUESTS:")
    print("-" * 50)
    for query in retrieval_queries:
        print(f"\nQuery: '{query}'")
        print(f"Should handle confidence: {agent.should_handle(query, {})}")
        
        result = agent.process(query, {})
        print(f"Response: {result['response']}")
        print(f"Memories used: {result.get('memories_used', [])}")
    
    # Check final memory state
    print("\nFINAL MEMORY STATE:")
    print("-" * 50)
    memories = memory.search_memories(topic="personal_info", limit=20)
    
    if memories:
        print(f"Found {len(memories)} personal info memories:")
        for memory in memories:
            print(f"- {memory['content']} (ID: {memory['id']}, Tags: {memory['tags']})")
    else:
        print("No personal info memories found!")
        
    print("\nTest completed!")

if __name__ == "__main__":
    test_agent_with_queries()