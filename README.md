# Amber.txt

An agent-based personal AI assistant that uses plain text for memory storage and specialized agents for contextual information retrieval.

## Overview

Amber.txt is designed to provide persistent personalization and deep contextual understanding of the user through:

- Plain text knowledge storage (JSON/YAML format)
- Contextual memory retrieval
- Specialized agent architecture
- Human-like conversation interface

## Key Features

- **Memory System**
   - Plain text knowledge store (JSON/YAML format)
   - Contextual memory retrieval with topic-based organization
   - Automatic memory tagging and categorization
   - Importance-based memory prioritization

- **Agent Architecture**
   - Dispatcher Agent: Routes queries to specialized agents
   - Personal Info Agent: Manages user details and preferences
   - General LLM Agent: Handles conversation and general queries
   - More specialized agents planned for future releases

- **Conversation Interface**
   - Streamlit-based chat interface
   - Memory references and citations
   - Context window management

## Setup & Installation

See the [Getting Started Guide](GETTING_STARTED.md) for detailed instructions on setting up and running Amber.txt.

Quick start:

```bash
# Clone the repository
git clone <repository-url>
cd <project-directory>

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the application
streamlit run app.py
```

## Project Structure

- `src/agents/` - Agent implementations
- `src/memory/` - Memory storage and retrieval
- `src/interface/` - User interface components
- `src/utils/` - Helper utilities

## Development Roadmap

1. **Core System** (Current Phase)
   - Chat interface, memory storage, dispatcher, basic agents

2. **Agent Expansion** (Upcoming)
   - Calendar and research agents
   - Memory tagging system
   - Confidence scoring

3. **Refinement** (Future)
   - Retrieval optimization
   - Forgetting curve
   - Memory correction mechanisms

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Insert License Information]