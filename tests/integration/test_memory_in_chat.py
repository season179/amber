"""
Test script for memory in a simulated chat context
"""
from src.memory.storage import MemoryStorage
from src.agents.personal_info_agent import PersonalInfoAgent
from src.agents.dispatcher import DispatcherAgent
from src.agents.llm_agent import LLMAgent
from src.utils.llm import LLMInterface

def simulate_chat():
    """
    Simulate a chat conversation and check if memory is working
    """
    import os
    from pathlib import Path

    # Use a dedicated test directory for integration tests
    tests_data_dir = Path(__file__).parent.parent / "data"
    if not tests_data_dir.exists():
        tests_data_dir.mkdir()

    test_dir = str(tests_data_dir / "chat_memory_store")
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    # Initialize components
    print("Initializing components...")
    memory_store = MemoryStorage(storage_dir=test_dir, format_type="json")
    
    # Create a mock LLM interface that doesn't actually call the API
    class MockLLMInterface(LLMInterface):
        def generate_response(self, messages, model=None, system_prompt=None):
            return {
                "content": "This is a mock response from the LLM.",
                "model": "mock-model",
                "usage": {"total_tokens": 0}
            }
    
    llm_interface = MockLLMInterface(api_key="mock-key", default_model="mock-model")
    
    # Create agents
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
    
    # Simulate a conversation
    messages = [
        "Remember that I live in San Francisco",
        "What's the weather like today?",
        "Remember that I'm allergic to peanuts",
        "Where do I live?",
        "What allergies do I have?"
    ]
    
    print("\nSimulating conversation...")
    for i, message in enumerate(messages):
        print(f"\nUser: {message}")
        
        # Build context
        context = {
            "conversation_history": conversation_history,
            "current_message_index": i
        }
        
        # Process message
        response_data = dispatcher.dispatch(message, context)
        
        # Add to conversation history
        conversation_history.append({"role": "user", "content": message})
        conversation_history.append({
            "role": "assistant", 
            "content": response_data["response"],
            "metadata": {
                "agent_id": response_data["agent_id"],
                "confidence": response_data["confidence"]
            }
        })
        
        print(f"Agent ({response_data['agent_id']}): {response_data['response']}")
        print(f"Confidence: {response_data['confidence']}")
        if 'memory_id' in response_data:
            print(f"Memory ID: {response_data['memory_id']}")
        if 'memories_used' in response_data:
            print(f"Memories used: {response_data['memories_used']}")
    
    # Check final memory state
    print("\nFinal memory state:")
    memories = memory_store.search_memories(topic="personal_info", limit=10)
    
    if memories:
        print(f"Found {len(memories)} personal info memories:")
        for memory in memories:
            print(f"- {memory['content']} (ID: {memory['id']}, Access count: {memory['access_count']})")
    else:
        print("No personal info memories found!")
        
    print("\nTest completed!")

if __name__ == "__main__":
    simulate_chat()