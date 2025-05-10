"""
Test script for the Streamlit app's memory functionality
"""
from src.interface.app import init_session_state, process_message
import streamlit as st

def test_app_memory():
    """Test the app's memory functionality"""
    import os
    from pathlib import Path

    # Use a dedicated test directory for app tests
    tests_data_dir = Path(__file__).parent.parent / "data"
    if not tests_data_dir.exists():
        tests_data_dir.mkdir()

    test_dir = str(tests_data_dir / "app_memory_store")
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    # Override the config to use our test directory
    import src.utils.config
    src.utils.config.get_storage_dir = lambda: test_dir

    print("Initializing app session state...")
    # Initialize the app state
    if not hasattr(st, "session_state"):
        st.session_state = {}
    
    init_session_state()
    
    # Check if memory_store was initialized
    if "memory_store" in st.session_state:
        print("Memory store initialized successfully")
    else:
        print("ERROR: Memory store not initialized")
        return
    
    # Check if dispatcher was initialized
    if "dispatcher" in st.session_state:
        print("Dispatcher initialized successfully")
    else:
        print("ERROR: Dispatcher not initialized")
        return
    
    # Simulate a user interaction that should store a memory
    test_input = "Remember that my favorite color is blue"
    
    print(f"\nProcessing test input: '{test_input}'")
    # Patch the streamlit components to avoid errors
    st.chat_message = lambda x: type('obj', (object,), {'write': lambda y: None, 'empty': lambda: type('obj', (object,), {'write': lambda z: None})})
    
    # Process the message
    try:
        process_message(test_input)
        print("Message processed successfully")
    except Exception as e:
        print(f"ERROR processing message: {e}")
        return
    
    # Check if the message was added to the conversation history
    if st.session_state.messages and len(st.session_state.messages) >= 2:
        print("Messages added to conversation history")
        print(f"User message: {st.session_state.messages[-2]['content']}")
        print(f"Response: {st.session_state.messages[-1]['content']}")
    else:
        print("ERROR: Messages not added to conversation history")
    
    # Check if a memory was stored
    memories = st.session_state.memory_store.search_memories(query="blue")
    if memories:
        print(f"\nFound {len(memories)} memories with 'blue':")
        for memory in memories:
            print(f"- {memory['content']} (ID: {memory['id']})")
    else:
        print("ERROR: No memories found with 'blue'")
    
    print("\nApp memory test completed!")

if __name__ == "__main__":
    test_app_memory()