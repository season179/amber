"""
Final integration test for Amber.txt memory system
"""
from src.memory.storage import MemoryStorage
from src.agents.personal_info_agent import PersonalInfoAgent
from src.agents.dispatcher import DispatcherAgent
from src.agents.llm_agent import LLMAgent
from src.utils.llm import LLMInterface

def test_final_integration():
    """
    Run a complete integration test for the memory system
    """
    # Clear existing test data from memory_store
    print("Initializing fresh memory store...")
    import os
    import shutil
    import json
    from pathlib import Path

    # Create a temporary directory within tests/data
    tests_data_dir = Path(__file__).parent.parent / "data"
    if not tests_data_dir.exists():
        tests_data_dir.mkdir()

    test_dir = str(tests_data_dir / "temp_memory_store")
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)
    
    # Initialize a fresh memory store
    memory_store = MemoryStorage(storage_dir=test_dir, format_type="json")
    
    # Create a mock LLM interface that doesn't call the API
    class MockLLMInterface(LLMInterface):
        def generate_response(self, messages, model=None, system_prompt=None):
            return {
                "content": "This is a mock response from the LLM.",
                "model": "mock-model",
                "usage": {"total_tokens": 0}
            }
    
    llm_interface = MockLLMInterface(api_key="mock-key", default_model="mock-model")
    
    # Create agents
    print("\nSetting up agents...")
    dispatcher = DispatcherAgent()
    personal_info_agent = PersonalInfoAgent(memory_store)
    llm_agent = LLMAgent(
        agent_id="general",
        name="General Assistant",
        description="I handle general conversation and queries.",
        llm_interface=llm_interface,
        memory_storage=memory_store
    )
    
    # Register agents
    dispatcher.register_agent(personal_info_agent)
    dispatcher.register_agent(llm_agent, is_fallback=True)
    
    # Initialize conversation history
    conversation_history = []
    
    # Test various memory storage patterns
    storage_queries = [
        "Remember that I live in Seattle",
        "I work at Microsoft",
        "Please remember I'm allergic to shellfish",
        "My favorite color is blue",
        "Just so you know my birthday is May 15",
        "My dog's name is Rex"
    ]
    
    memory_ids = []
    
    print("\nTESTING MEMORY STORAGE:")
    print("-" * 50)
    for query in storage_queries:
        print(f"\nQuery: '{query}'")
        
        # Process with personal info agent directly to check storage
        result = personal_info_agent.process(query, {"conversation_history": []})
        print(f"Agent: {result['response']}")
        
        if 'memory_id' in result:
            memory_ids.append(result['memory_id'])
            print(f"Memory ID: {result['memory_id']}")
        else:
            print(f"Memory ID: None")
    
    # Verify unique IDs
    print(f"\nNumber of unique memory IDs: {len(set(memory_ids))}")
    print(f"Number of memory storage requests: {len(storage_queries)}")
    assert len(set(memory_ids)) == len(memory_ids), "Memory IDs are not unique!"
    
    # Test retrievals with the dispatcher
    retrieval_queries = [
        "Where do I live?",
        "Where do I work?",
        "Do I have any allergies?",
        "What is my favorite color?",
        "When is my birthday?",
        "What's my dog's name?"
    ]
    
    print("\n\nTESTING MEMORY RETRIEVAL:")
    print("-" * 50)
    for query in retrieval_queries:
        print(f"\nQuery: '{query}'")
        
        # Build context
        context = {"conversation_history": conversation_history}
        
        # Process with dispatcher
        response_data = dispatcher.dispatch(query, context)
        
        print(f"Selected agent: {response_data['agent_id']}")
        print(f"Confidence: {response_data['confidence']}")
        print(f"Response: {response_data['response']}")
        
        if 'memories_used' in response_data:
            print(f"Memories used: {response_data['memories_used']}")
    
    # Check memory files
    print("\n\nFINAL MEMORY STATE:")
    print("-" * 50)
    
    # Check general memory file
    general_path = os.path.join(test_dir, "general.json")
    with open(general_path, 'r') as f:
        general_data = json.load(f)
    
    print(f"General memories: {len(general_data['memories'])}")
    for memory in general_data['memories']:
        print(f"- {memory['content']} (ID: {memory['id']})")
    
    # Check topic files
    topic_path = os.path.join(test_dir, "topic_personal_info.json")
    if os.path.exists(topic_path):
        with open(topic_path, 'r') as f:
            topic_data = json.load(f)
        
        print(f"\nPersonal info memories: {len(topic_data['memories'])}")
        for memory in topic_data['memories']:
            print(f"- {memory['content']} (ID: {memory['id']}, Access count: {memory['access_count']})")
    
    print("\nIntegration test completed successfully!")

if __name__ == "__main__":
    test_final_integration()