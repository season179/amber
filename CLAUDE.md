# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Amber.txt is an agent-based personal AI assistant that uses plain text for memory storage and specialized agents for contextual information retrieval. The system aims to provide persistent personalization and deep contextual understanding of the user.

## Architecture

The architecture consists of several key components:

1. **Memory System**
   - Plain text knowledge store (JSON/YAML format)
   - Contextual memory retrieval with topic-based and temporal organization
   - Automatic memory tagging and categorization
   - Forgetting curve implementation to prioritize important/recent information

2. **Agent Architecture**
   - Dispatcher Agent: Routes queries to specialized agents
   - Personal Info Agent: Manages user details and preferences
   - Calendar Agent: Handles time-based information
   - Research Agent: Searches web/documents for needed context
   - Summarization Agent: Condenses long-term history

3. **Interface Components**
   - Context window management
   - Memory references and citations
   - Confidence indicators
   - Correction mechanisms for user feedback

## Technology Stack

- **Frontend:** Streamlit
- **Backend:** Python 3.11 with virtual environment
- **LLM Provider:** OpenRouter
- **Storage:** Local file system (prototype)

## Development Workflow

For this early-stage project (currently at PRD stage), the following workflow will likely be relevant:

### Environment Setup
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies (when requirements.txt is available)
pip install -r requirements.txt
```

### Running the Application
```bash
# When implemented, the application will likely use Streamlit
streamlit run app.py
```

## Development Phases

The project is planned in three phases:
1. **Core System** (2 weeks): Chat interface, memory storage, dispatcher, basic agent
2. **Agent Expansion** (2 weeks): Additional agents, memory tagging, confidence scoring
3. **Refinement** (2 weeks): Optimization, forgetting curve, memory correction

## Project Structure

As the project develops, it will likely follow a structure with:
- Agent modules for different specialized functions
- Memory management system
- Context handling mechanisms
- LLM interface for prompt engineering and API calls