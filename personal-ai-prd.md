# Product Requirements Document: Agent-Based Personal AI Assistant

## 1. Product Overview
**Product Name:** Amber.txt  
**Version:** 0.1 (Prototype)  
**Date:** May 10, 2025

### 1.1 Problem Statement
Current AI assistants lack persistent personalization and deep contextual understanding of the user. They either forget previous interactions or require complex indexing systems that limit flexibility. Users need an assistant that builds knowledge about them organically and recalls information contextually without heavyweight infrastructure.

### 1.2 Product Vision
An agentic personal AI assistant that stores memories as plain text and uses specialized agents to retrieve and apply relevant information when needed, creating a more human-like, adaptive experience that grows with the user.

### 1.3 Target Users
- Knowledge workers managing complex information
- Personal productivity enthusiasts
- Early adopters of AI technology

## 2. Key Features (Shaped Bets)

### 2.1 Memory System
- **Plain Text Knowledge Store:** Structured JSON/YAML for memories
- **Contextual Memory Retrieval:** Topic-based and temporal organization
- **Memory Tagging:** Automatic categorization of information
- **Forgetting Curve:** Prioritize important/recent information

### 2.2 Agent Architecture
- **Dispatcher Agent:** Routes queries to specialized agents
- **Personal Info Agent:** Manages user details and preferences
- **Calendar Agent:** Handles time-based information
- **Research Agent:** Searches web/documents for needed context
- **Summarization Agent:** Condenses long-term history

### 2.3 Conversation Interface
- **Context Window Management:** Maintain important context
- **Memory References:** Cite sources of recalled information
- **Confidence Indicators:** Show certainty of recalled information
- **Correction Mechanisms:** User feedback improves memory

## 3. User Experience

### 3.1 Conversation Flow
1. User enters query
2. System parses intent and context needs
3. Dispatcher activates relevant agents
4. Agents retrieve context from plain text stores
5. Response integrates agent results and builds on conversation

### 3.2 Memory Management
- Users can view stored memories
- Direct editing/deletion of specific memories
- Memory importance flagging
- Privacy controls for sensitive information

## 4. Technical Architecture

### 4.1 Technology Stack
- **Frontend:** Streamlit
- **Backend:** Python 3.11 with virtual environment
- **LLM Provider:** OpenRouter
- **Storage:** Local file system (prototype), expandable to cloud

### 4.2 System Components
- **Memory Storage Module:** Organizes plain text memory
- **Agent Framework:** Orchestrates specialized agents
- **Context Manager:** Maintains conversation state
- **LLM Interface:** Handles prompt engineering and API calls

### 4.3 Data Flow
1. User input → Intent classification
2. Intent → Agent selection
3. Agents → Memory retrieval
4. Memory + Input → LLM context window
5. LLM response → User + Memory update

## 5. Development Phases

### 5.1 Phase 1: Core System (2 weeks)
- Implement basic chat interface
- Develop memory storage format
- Create dispatcher and basic personal info agent
- Establish conversation flow

### 5.2 Phase 2: Agent Expansion (2 weeks)
- Implement calendar and research agents
- Develop memory tagging system
- Build confidence scoring
- Create memory visualization

### 5.3 Phase 3: Refinement (2 weeks)
- Optimize retrieval performance
- Implement forgetting curve
- Add memory correction mechanisms
- Polish UI and documentation

## 6. Success Metrics

### 6.1 Technical Metrics
- Memory retrieval accuracy
- Retrieval latency < 2 seconds
- Agent coordination reliability
- System stability

### 6.2 User Experience Metrics
- Conversation naturalness
- Information recall relevance
- Personalization accuracy
- User trust development

## 7. Limitations and Future Expansion

### 7.1 Prototype Limitations
- Text-only interface
- Limited agent complexity
- Local deployment
- English language only

### 7.2 Future Expansion
- Voice interface
- More specialized agents
- Multi-modal inputs
- Enhanced privacy features
- Cloud syncing
