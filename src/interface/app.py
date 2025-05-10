"""
Streamlit interface for Amber.txt personal AI assistant
"""
import streamlit as st
import time
from datetime import datetime
import json
import os
from typing import Dict, List, Any

# Import from our modules
try:
    # Try relative imports first (when run as a module)
    from ..memory.storage import MemoryStorage
    from ..agents.personal_info_agent import PersonalInfoAgent
    from ..agents.dispatcher import DispatcherAgent
    from ..agents.llm_agent import LLMAgent
    from ..utils.config import get_storage_dir, get_storage_format
    from ..utils.llm import LLMInterface
except ImportError:
    # Fall back to absolute imports (when run directly)
    from src.memory.storage import MemoryStorage
    from src.agents.personal_info_agent import PersonalInfoAgent
    from src.agents.dispatcher import DispatcherAgent
    from src.agents.llm_agent import LLMAgent
    from src.utils.config import get_storage_dir, get_storage_format
    from src.utils.llm import LLMInterface


# Initialize the application state
def init_session_state():
    """Initialize Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "memory_store" not in st.session_state:
        storage_dir = get_storage_dir()
        storage_format = get_storage_format()
        st.session_state.memory_store = MemoryStorage(
            storage_dir=storage_dir,
            format_type=storage_format
        )
    
    if "llm_interface" not in st.session_state:
        st.session_state.llm_interface = LLMInterface()
    
    if "dispatcher" not in st.session_state:
        # Create and initialize the dispatcher with agents
        dispatcher = DispatcherAgent()
        
        # Create the LLM agent (fallback agent)
        llm_agent = LLMAgent(
            agent_id="general",
            name="General Assistant",
            description="I handle general conversation and queries.",
            llm_interface=st.session_state.llm_interface,
            memory_storage=st.session_state.memory_store
        )
        
        # Create and register the personal info agent
        personal_info_agent = PersonalInfoAgent(st.session_state.memory_store)
        
        # Register agents with the dispatcher
        dispatcher.register_agent(personal_info_agent)
        dispatcher.register_agent(llm_agent, is_fallback=True)
        
        st.session_state.dispatcher = dispatcher


# Set up the Streamlit UI
def setup_ui():
    """Configure the Streamlit UI components."""
    st.set_page_config(
        page_title="Amber.txt - Personal AI Assistant",
        page_icon="🔸",
        layout="wide"
    )
    
    st.title("🔸 Amber.txt")
    st.caption("Your personal AI assistant with contextual memory")
    
    # Sidebar for configuration and memory viewing
    with st.sidebar:
        st.header("Memory Explorer")
        if st.button("View Recent Memories"):
            display_memories()
        
        # Add a divider
        st.divider()
        
        # System information
        st.header("System Info")
        st.write(f"Running in: {get_storage_dir()}")
        st.write(f"Storage Format: {get_storage_format()}")
        
        # Additional sidebar elements can be added here
        st.divider()
        
        # About section
        st.header("About")
        st.write("""
        Amber.txt is an agent-based personal AI assistant that uses plain text
        for memory storage and specialized agents for contextual information retrieval.
        """)


# Display memories from the memory store
def display_memories():
    """Display recent memories from the memory store."""
    memories = st.session_state.memory_store.search_memories(limit=10)
    
    if not memories:
        st.sidebar.write("No memories found.")
        return
    
    for memory in memories:
        with st.sidebar.expander(f"{memory['content'][:30]}...", expanded=False):
            st.write(f"**Content:** {memory['content']}")
            st.write(f"**Created:** {memory['created_at']}")
            st.write(f"**Tags:** {', '.join(memory['tags'])}")
            st.write(f"**Importance:** {memory['importance']}/10")


# Process a user message and update the UI
def process_message(user_input: str):
    """
    Process a user message through the agent system.
    
    Args:
        user_input: The user's input message
    """
    if not user_input.strip():
        return
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Show a thinking indicator
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.write("Thinking...")
    
    # Prepare context from conversation history
    context = {
        "conversation_history": st.session_state.messages,
        "current_time": datetime.now().isoformat()
    }
    
    # Process the query through our dispatcher
    response_data = st.session_state.dispatcher.dispatch(user_input, context)
    
    # Replace thinking indicator with actual response
    message_placeholder.write(response_data["response"])
    
    # Add assistant response to chat history
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response_data["response"],
        "metadata": {
            "agent_id": response_data["agent_id"],
            "confidence": response_data["confidence"],
            "timestamp": datetime.now().isoformat()
        }
    })


def main():
    """Main application entry point."""
    # Initialize session state
    init_session_state()
    
    # Set up the UI
    setup_ui()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Input for new message
    user_input = st.chat_input("How can I assist you today?")
    if user_input:
        process_message(user_input)
        # Force a rerun to update the UI immediately
        st.rerun()


if __name__ == "__main__":
    main()