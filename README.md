# Account Brief Generator

A Python CLI tool that generates structured account briefs to help Account Executives quickly prepare for outbound outreach and discovery calls.

## What It Does

Generates a comprehensive account brief in markdown format with:
- **Account Overview** - Company, persona, and competitive landscape
- **Why Now Triggers** - Timing factors and outreach triggers
- **Persona Pain Points** - Role-specific challenges and frustrations
- **5 Discovery Questions** - Structured questions for discovery calls
- **3-Email Outbound Sequence** - Complete email templates (initial, follow-up, final)
- **1 LinkedIn Message** - LinkedIn outreach template
- **Objection Handling** - Common objections with response templates

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py --company "Acme Corp" --persona "CTO" --competitor "VendorX, CompetitorY"
```

**Short options:**
```bash
python main.py -c "Ramp" -p "CTO" -co "GitHub Copilot, Windsurf"
```

**Arguments:**
- `--company`, `-c`: Company name (required)
- `--persona`, `-p`: Target persona (required)
- `--competitor`, `-co`: Competitor name(s), comma-separated (optional)
- `--llm`: Use LLM to research persona names (choices: `openai` or `anthropic`). Requires API key in environment variable.

**Output:** Saves to `outputs/<company>/<company>-v<N>.md`

**LLM Integration (Optional):**
To get actual persona names (e.g., "CTO: John Smith"), use the `--llm` flag:

```bash
# With OpenAI (ChatGPT)
export OPENAI_API_KEY="your-api-key"
python main.py -c "Ramp" -p "CTO" --llm openai

# With Anthropic (Claude)
export ANTHROPIC_API_KEY="your-api-key"
python main.py -c "Ramp" -p "CTO" --llm anthropic
```

## Why It's Useful for AEs

**Save Time:** Generate a complete account brief in seconds instead of manually researching and drafting outreach materials.

**Stay Consistent:** Every brief follows the same structure, ensuring you don't miss critical elements like discovery questions or objection handling.

**Scale Outreach:** Quickly prepare personalized outbound sequences for multiple accounts without starting from scratch.

**Be Prepared:** Have objection responses, discovery questions, and email templates ready before your first interaction.

**Focus on Execution:** Spend less time on prep work and more time on selling. Fill in the template placeholders with account-specific research and start outreach immediately.
