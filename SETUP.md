# Setup Guide - MoZilla

Quick setup instructions to get MoZilla running on your machine.

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/MohamedNSoliman/account-brief-generator.git
cd account-brief-generator
```

### 2. Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

Or if you prefer using `python3 -m pip`:

```bash
python3 -m pip install -r requirements.txt
```

### 3. Run the App

Start the Streamlit web application:

```bash
python3 -m streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## Optional: Set Up Virtual Environment (Recommended)

Using a virtual environment keeps your project dependencies isolated:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python3 -m streamlit run app.py
```

## Optional: Enable LLM Features

To use enhanced features (persona name detection, personalized emails, etc.), you'll need an API key from either OpenAI or Anthropic.

### With OpenAI:

1. Get your API key from [OpenAI](https://platform.openai.com/api-keys)
2. Set it as an environment variable:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

### With Anthropic (Claude):

1. Get your API key from [Anthropic](https://console.anthropic.com/)
2. Set it as an environment variable:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

**Note:** You can also enter your API key directly in the app's settings sidebar (it's not stored permanently).

## First Run

1. When you first open the app, you'll see a login/register page
2. Create a new account by clicking the "Register" tab
3. Enter a username and password
4. After registering, you'll be logged in automatically
5. Start generating account briefs!

## Troubleshooting

### "Command not found: streamlit"

Make sure you've installed dependencies:
```bash
pip install -r requirements.txt
```

If you're in a virtual environment, make sure it's activated and dependencies are installed there.

### "Module not found" errors

Reinstall dependencies:
```bash
pip install -r requirements.txt
```

### Port already in use

If port 8501 is already in use, Streamlit will automatically try the next available port. Check the terminal output for the actual URL.

### Database errors

The database (`data/account_briefs.db`) is created automatically on first run. If you encounter database errors, try deleting the `data/` folder and restarting the app.

## What Gets Installed

The following packages are installed when you run `pip install -r requirements.txt`:

- **streamlit** - Web framework for the app
- **pydantic** - Data validation
- **requests** - HTTP library
- **duckduckgo-search** - Web search functionality
- **openai** (optional) - For OpenAI/ChatGPT integration
- **anthropic** (optional) - For Claude/Anthropic integration

## Need Help?

- Check the main [README.md](README.md) for more detailed documentation
- Open an issue on GitHub if you encounter problems
- Review the [README_WEB_APP.md](README_WEB_APP.md) for deployment options

## Next Steps

Once the app is running:

1. Create an account or log in
2. Try generating a brief for a company (e.g., type "Ramp" in the chat)
3. Explore the settings to enable web research or LLM features
4. Save your briefs for later reference

Enjoy using MoZilla! 🦎
