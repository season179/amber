# Getting Started with Amber.txt

This guide will help you set up and run the Amber.txt personal AI assistant.

## Prerequisites

- Python 3.11 or higher
- OpenRouter API key (sign up at [openrouter.ai](https://openrouter.ai/))

## Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd <project-directory>
```

2. **Set up a virtual environment**

```bash
# Create the virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

Alternatively, you can install the package in development mode:

```bash
pip install -e .
```

4. **Configure environment variables**

Copy the example environment file and fill in your API keys:

```bash
cp .env.example .env
```

Then edit the `.env` file with your preferred text editor to add your OpenRouter API key:

```
OPENROUTER_API_KEY=your_api_key_here
```

## Running the Application

Start the Streamlit application:

```bash
# Make sure you're in the project directory and your virtual environment is activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the application
streamlit run app.py
```

The application will be accessible at http://localhost:8501 in your web browser.

## Using Amber.txt

### Basic Interaction

Simply type your messages in the chat input at the bottom of the page. Amber.txt will respond based on:

1. Your conversation history
2. Personal information you've shared
3. Contextual understanding of your queries

### Storing Personal Information

To help Amber.txt remember details about you, phrase your messages like:

- "Remember that I prefer dark chocolate over milk chocolate."
- "Make note that my favorite color is blue."
- "Keep in mind that I'm allergic to shellfish."

### Retrieving Information

To access stored information, simply ask naturally:

- "What are my food preferences?"
- "What's my favorite color?"
- "What am I allergic to?"

### Viewing Stored Memories

You can view your stored memories by clicking the "View Recent Memories" button in the sidebar.

## Troubleshooting

### API Key Issues

If you see errors related to OpenRouter API access:

1. Check that your API key is correctly set in the `.env` file
2. Verify that your OpenRouter account is active
3. Check OpenRouter's status page for any service disruptions

### Application Crashes

If the application crashes:

1. Check the terminal for error messages
2. Ensure all dependencies are correctly installed
3. Verify that you're using Python 3.11 or higher

## Next Steps

As Amber.txt is actively being developed, you can look forward to:

- Additional specialized agents (Calendar, Research, Summarization)
- Enhanced memory tagging and organization
- Confidence indication for recalled information
- Memory editing and correction mechanisms