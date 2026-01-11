# Account Brief Generator

A Python CLI tool and web app that generates structured account briefs to help Account Executives quickly prepare for outbound outreach and discovery calls.

## What It Does

Generates a comprehensive account brief in markdown format with:
- **Account Overview** - Company, persona, and competitive landscape
- **Why Now Triggers** - Timing factors and outreach triggers
- **Persona Pain Points** - Role-specific challenges and frustrations
- **5 Discovery Questions** - Structured questions for discovery calls
- **3-Email Outbound Sequence** - Complete email templates (initial, follow-up, final)
- **1 LinkedIn Message** - LinkedIn outreach template
- **Objection Handling** - Common objections with response templates

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

## Installation

📋 **New to MoZilla?** Check out the [SETUP.md](SETUP.md) guide for detailed setup instructions!

1. **Clone the repository:**
```bash
git clone https://github.com/MohamedNSoliman/account-brief-generator.git
cd account-brief-generator
```

2. **Create a virtual environment (recommended):**
```bash
python3 -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Optional: Install LLM dependencies** (for enhanced features):
```bash
# For OpenAI
pip install openai>=1.0.0

# For Anthropic
pip install anthropic>=0.18.0
```

## Usage

### CLI (Command Line)

```bash
python main.py --company "Acme Corp" --persona "Head of Engineering" --competitor "VendorX, CompetitorY"
```

**Short options:**
```bash
python main.py -c "Ramp" -p "VP Engineering" -co "GitHub Copilot, Windsurf"
```

**Arguments:**
- `--company`, `-c`: Company name (required)
- `--persona`, `-p`: Target persona (required). Recommended: Head of Engineering, VP Engineering, Developer Experience Lead, Platform Lead, Engineering Productivity
- `--competitor`, `-co`: Competitor name(s), comma-separated (optional, default: "Unknown")
- `--no-research`: Skip web research and use template placeholders only
- `--llm`: Use LLM to research persona names and enhance content (choices: `openai` or `anthropic`). Requires API key in environment variable.

**Output:** Saves to `outputs/<company>/<company>-v<N>.md`

### Web App (Streamlit)

Run the web interface:

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

See [README_WEB_APP.md](README_WEB_APP.md) for deployment options.

### LLM Integration (Optional)

To get actual persona names and enhanced, personalized content, use the `--llm` flag:

```bash
# With OpenAI (ChatGPT)
export OPENAI_API_KEY="your-api-key"
python main.py -c "Ramp" -p "Head of Engineering" --llm openai

# With Anthropic (Claude)
export ANTHROPIC_API_KEY="your-api-key"
python main.py -c "Ramp" -p "VP Engineering" --llm anthropic
```

**What LLM integration adds:**
- Real persona names (e.g., "VP Engineering: Jane Smith")
- Detailed company information (size, funding, revenue, tech stack)
- Personalized email sequences (no placeholders, company-specific)
- Enhanced LinkedIn messages

## Why It's Useful for AEs

**Save Time:** Generate a complete account brief in seconds instead of manually researching and drafting outreach materials.

**Stay Consistent:** Every brief follows the same structure, ensuring you don't miss critical elements like discovery questions or objection handling.

**Scale Outreach:** Quickly prepare personalized outbound sequences for multiple accounts without starting from scratch.

**Be Prepared:** Have objection responses, discovery questions, and email templates ready before your first interaction.

**Focus on Execution:** Spend less time on prep work and more time on selling. Fill in the template placeholders with account-specific research and start outreach immediately.
