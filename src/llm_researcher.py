"""
LLM-based research module for gathering persona and company information.
"""

import os
from typing import Dict, List, Optional

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


def get_openai_client():
    """Get OpenAI client if API key is available."""
    if not OPENAI_AVAILABLE:
        return None
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return None
    return openai.OpenAI(api_key=api_key)


def get_anthropic_client():
    """Get Anthropic client if API key is available."""
    if not ANTHROPIC_AVAILABLE:
        return None
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        return None
    return anthropic.Anthropic(api_key=api_key)


def research_persona_with_llm(company: str, persona: str, provider: str = "openai") -> Dict[str, any]:
    """
    Research persona information using LLM.
    
    Args:
        company: Company name
        persona: Persona/role (e.g., "CTO", "VP Engineering")
        provider: LLM provider ("openai" or "anthropic")
        
    Returns:
        Dictionary with persona information including name if found
    """
    prompt = f"""Research the {persona} at {company}. Provide the following information in a structured format:
1. Name of the {persona} (if publicly available)
2. Key background/experience relevant to this role
3. Recent public statements or content they've shared
4. Their focus areas and priorities

Format your response as:
NAME: [name or "Not publicly available"]
BACKGROUND: [brief background]
FOCUS: [key focus areas]"""

    if provider == "openai":
        client = get_openai_client()
        if not client:
            return {"name": None, "error": "OpenAI API key not found. Set OPENAI_API_KEY environment variable."}
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a research assistant that helps find information about executives and their companies."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            content = response.choices[0].message.content
            return parse_llm_response(content)
        except Exception as e:
            return {"name": None, "error": f"OpenAI API error: {str(e)}"}
    
    elif provider == "anthropic":
        client = get_anthropic_client()
        if not client:
            return {"name": None, "error": "Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable."}
        
        try:
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            content = message.content[0].text
            return parse_llm_response(content)
        except Exception as e:
            return {"name": None, "error": f"Anthropic API error: {str(e)}"}
    
    return {"name": None, "error": f"Unknown provider: {provider}"}


def parse_llm_response(content: str) -> Dict[str, any]:
    """Parse LLM response into structured format."""
    result = {
        "name": None,
        "background": None,
        "focus": None,
        "raw_response": content
    }
    
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('NAME:'):
            name = line.replace('NAME:', '').strip()
            if name and name.lower() not in ['not publicly available', 'n/a', 'unknown']:
                result["name"] = name
        elif line.startswith('BACKGROUND:'):
            result["background"] = line.replace('BACKGROUND:', '').strip()
        elif line.startswith('FOCUS:'):
            result["focus"] = line.replace('FOCUS:', '').strip()
    
    return result


def research_company_context_with_llm(company: str, provider: str = "openai") -> Dict[str, any]:
    """
    Research comprehensive company information for account briefing.
    
    Args:
        company: Company name
        provider: LLM provider ("openai" or "anthropic")
        
    Returns:
        Dictionary with comprehensive company information
    """
    prompt = f"""Research {company} and provide comprehensive account intelligence information. Be specific and accurate. Every detail must be unique to {company} - avoid generic information that could apply to any company.

1. Company Description: What does {company} do? (1-2 sentences, specific to {company})
2. Company Size: Total number of employees (approximate if exact not available)
3. Engineering Team Size: Number of engineers/developers (approximate)
4. Funding: Latest funding round (Series, amount, date, investors if known)
5. Revenue: Revenue range or ARR if available (if private, estimate if possible)
6. Headquarters: Location
7. Key Executives: List CTO, VP Engineering, and other relevant tech executives with names if available
8. Recent News: Key developments in last 6-12 months (specific to {company})
9. Technology Stack: Primary technologies/tools they use (if known, specific to {company})
10. Key Differentiators: What makes {company} unique (not generic industry characteristics)

CRITICAL: If any information feels generic or could apply to multiple companies, make it more specific to {company} only.

Format your response as:
DESCRIPTION: [what they do]
EMPLOYEES: [number or range]
ENGINEERING_TEAM: [number or range]
FUNDING: [latest round details]
REVENUE: [revenue/ARR information]
HEADQUARTERS: [location]
EXECUTIVES: [list of key executives with titles and names]
RECENT_NEWS: [recent developments]
TECH_STACK: [technologies used]
DIFFERENTIATORS: [key unique aspects]"""

    if provider == "openai":
        client = get_openai_client()
        if not client:
            return {"error": "OpenAI API key not found"}
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a research assistant that helps find detailed company information for sales and marketing purposes. Provide information that is specific and unique to each company - avoid generic details that could apply to any company."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            content = response.choices[0].message.content
            return parse_company_context(content)
        except Exception as e:
            return {"error": f"OpenAI API error: {str(e)}"}
    
    elif provider == "anthropic":
        client = get_anthropic_client()
        if not client:
            return {"error": "Anthropic API key not found"}
        
        try:
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=800,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            content = message.content[0].text
            return parse_company_context(content)
        except Exception as e:
            return {"error": f"Anthropic API error: {str(e)}"}
    
    return {"error": f"Unknown provider: {provider}"}


def parse_company_context(content: str) -> Dict[str, any]:
    """Parse company context from LLM response."""
    result = {
        "description": None,
        "employees": None,
        "engineering_team": None,
        "funding": None,
        "revenue": None,
        "headquarters": None,
        "executives": None,
        "recent_news": None,
        "tech_stack": None,
        "differentiators": None,
        "raw_response": content
    }
    
    lines = content.split('\n')
    current_key = None
    current_value = []
    
    for line in lines:
        line = line.strip()
        if ':' in line and not line.startswith(' '):
            # Save previous value
            if current_key:
                key_name = current_key.lower().replace(' ', '_')
                result[key_name] = ' '.join(current_value).strip()
            
            # Start new key
            parts = line.split(':', 1)
            current_key = parts[0].upper().replace(' ', '_')
            current_value = [parts[1].strip()] if len(parts) > 1 and parts[1].strip() else []
        elif current_key and line:
            current_value.append(line)
    
    # Save last value
    if current_key:
        key_name = current_key.lower().replace(' ', '_')
        result[key_name] = ' '.join(current_value).strip()
    
    return result


def enhance_brief_with_llm(company: str, persona: str, competitors: List[str], 
                           use_persona_research: bool = True, provider: str = "openai") -> Dict[str, any]:
    """
    Enhance account brief with LLM-generated content.
    
    Args:
        company: Company name
        persona: Persona/role
        competitors: List of competitors
        use_persona_research: Whether to research persona name
        provider: LLM provider ("openai" or "anthropic")
        
    Returns:
        Dictionary with enhanced content
    """
    enhanced = {
        "persona_name": None,
        "persona_background": None,
        "persona_focus": None,
        "company_description": None,
        "company_employees": None,
        "company_engineering_team": None,
        "company_funding": None,
        "company_revenue": None,
        "company_headquarters": None,
        "company_executives": None,
        "company_recent_news": None,
        "company_tech_stack": None,
        "company_differentiators": None
    }
    
    if use_persona_research:
        # Research comprehensive company context first (this includes executives)
        company_context = research_company_context_with_llm(company, provider)
        if "error" not in company_context:
            enhanced["company_description"] = company_context.get("description")
            enhanced["company_employees"] = company_context.get("employees")
            enhanced["company_engineering_team"] = company_context.get("engineering_team")
            enhanced["company_funding"] = company_context.get("funding")
            enhanced["company_revenue"] = company_context.get("revenue")
            enhanced["company_headquarters"] = company_context.get("headquarters")
            enhanced["company_executives"] = company_context.get("executives")
            enhanced["company_recent_news"] = company_context.get("recent_news")
            enhanced["company_tech_stack"] = company_context.get("tech_stack")
            enhanced["company_differentiators"] = company_context.get("differentiators")
            
            # Extract persona name from executives list if available
            executives_str = enhanced["company_executives"]
            if executives_str:
                # Try to find the persona in the executives list
                persona_lower = persona.lower()
                for line in executives_str.split('\n'):
                    if persona_lower in line.lower():
                        # Extract name (typically format: "Name, Title" or "Title: Name")
                        parts = line.split(',')
                        if len(parts) > 1:
                            enhanced["persona_name"] = parts[0].strip()
                        else:
                            parts = line.split(':')
                            if len(parts) > 1:
                                enhanced["persona_name"] = parts[1].strip()
                        break
        
        # Also try direct persona research as fallback
        if not enhanced.get("persona_name"):
            persona_info = research_persona_with_llm(company, persona, provider)
            if persona_info.get("name"):
                enhanced["persona_name"] = persona_info.get("name")
            enhanced["persona_background"] = persona_info.get("background")
            enhanced["persona_focus"] = persona_info.get("focus")
    
    return enhanced


def generate_email_sequence_with_llm(company: str, persona: str, persona_name: str, 
                                     company_info: Dict[str, any], competitors: List[str],
                                     pain_points: List[str], provider: str = "openai") -> Dict[str, str]:
    """
    Generate complete email sequences using LLM - no placeholders, real AE-style emails.
    
    Args:
        company: Company name
        persona: Persona/role
        persona_name: Name of the persona (if known)
        company_info: Dictionary with company research data
        competitors: List of competitors
        pain_points: List of pain points for the persona
        provider: LLM provider
        
    Returns:
        Dictionary with email subject, body, and follow-up emails
    """
    greeting = persona_name if persona_name else "[First Name]"
    company_desc = company_info.get("description", "")
    recent_news = company_info.get("recent_news", "")
    funding = company_info.get("funding", "")
    
    prompt = f"""You are an enterprise Account Executive at Cursor selling a developer tool to engineering teams. Cursor uses a PRODUCT-LED GROWTH (PLG) motion, not sales-led.

Company: {company}
Persona: {persona_name if persona_name else persona}
Competitors: {', '.join(competitors) if competitors else 'Unknown'}
{f"Company description: {company_desc}" if company_desc else ""}
{f"Recent news: {recent_news}" if recent_news else ""}
{f"Funding: {funding}" if funding else ""}
Key pain points: {', '.join(pain_points[:3]) if pain_points else 'Standard industry challenges'}

IMPORTANT CONTEXT - PLG Motion:
- Teams likely have trial users, free users, or are evaluating Cursor
- Focus on activation, expansion, and helping existing users get more value
- Less "cold discovery" - more "I noticed you're trying/evaluating, here's how to maximize value"
- Reference product usage patterns, adoption signals, or evaluation stages when relevant
- Emphasize helping teams scale usage and get ROI, not just introducing the product
- Write for tactical, implementation-focused engineering leaders (Head of Engineering, VP Engineering, Developer Experience Lead, Platform Lead, Engineering Productivity), NOT strategic execs

Rules:
- Do NOT use placeholders like [customize], [add value], or brackets
- Do NOT use generic phrases like "industry trends suggest" or "companies like yours"
- Do NOT use generic CTAs like "Would you be open to a 15 minute conversation" or "Let's schedule a call"
- Do NOT use strategic/vague language - be tactical and concrete
- CRITICAL: If any section feels generic or could apply to any company/persona, rewrite it until it could ONLY apply to {company} and {persona_name if persona_name else persona}
- Every detail must be specific to {company}'s business, recent news, funding, team size, or engineering challenges
- Be concrete, specific, and opinionated about developer tools and engineering workflows
- Assume the reader is smart and busy, focused on implementation
- Tone: direct, sharp, professional, engineering-focused
- Max 90 words per email
- No hype
- No "hope you're well"
- Reference competitors directly where relevant ({', '.join(competitors) if competitors else 'their current tools'})
- When mentioning competitors, explain how the product would be evaluated against them and what tradeoffs the persona would care about
- Don't just name competitors - provide contrast: what tradeoffs matter (speed vs. accuracy, local vs. cloud, code snippets vs. full repo context, etc.)
- CTAs should be value-driven: explain how you differ from competitors, offer a specific insight, or provide a concrete comparison with tradeoffs
- Example good CTA: "If you're already evaluating {', '.join(competitors[:2]) if competitors else 'Copilot or Windsurf'}, it might be useful to compare how [product] differs in [specific way] and the tradeoffs you'd consider (e.g., [specific tradeoff relevant to persona])."

Write 3 complete emails and 1 LinkedIn message. Each email must be sendable as-is.

PLG Context: Emails should reference that the team might be trying/evaluating Cursor, help them get more value, or focus on expansion/activation rather than pure cold outreach.

Format as:
EMAIL1_SUBJECT: [subject line]
EMAIL1_BODY: [complete email body, max 90 words]

EMAIL2_SUBJECT: [subject line]
EMAIL2_BODY: [complete email body, max 90 words]

EMAIL3_SUBJECT: [subject line]
EMAIL3_BODY: [complete email body, max 90 words]

LINKEDIN_MESSAGE: [short, natural LinkedIn message]"""

    if provider == "openai":
        client = get_openai_client()
        if not client:
            return {"error": "OpenAI API key not found"}
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an enterprise Account Executive at Cursor (product-led growth company) selling developer tools to engineering teams. Write direct, sharp, professional emails with zero placeholders. Cursor uses PLG - focus on activation, expansion, and helping existing/trial users get more value, not pure cold discovery. Target tactical, implementation-focused engineering leaders (Head of Engineering, VP Engineering, Developer Experience Lead, Platform Lead, Engineering Productivity), NOT strategic execs. Be concrete, specific, and opinionated about developer tools and engineering workflows. Avoid strategic/vague language. Assume the reader is smart and busy. Max 90 words per email. No hype, no pleasantries like 'hope you're well'. When mentioning competitors, explain how the product would be evaluated against them and what tradeoffs the persona would care about (speed vs accuracy, local vs cloud, snippets vs full repo context, etc.). CTAs must be value-driven comparisons or insights with tradeoffs, NOT generic meeting requests like 'would you be open to a call'."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            content = response.choices[0].message.content
            return parse_email_sequence(content, greeting)
        except Exception as e:
            return {"error": f"OpenAI API error: {str(e)}"}
    
    elif provider == "anthropic":
        client = get_anthropic_client()
        if not client:
            return {"error": "Anthropic API key not found"}
        
        try:
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                system="You are an enterprise Account Executive at Cursor (product-led growth company) selling developer tools to engineering teams. Write direct, sharp, professional emails with zero placeholders. Cursor uses PLG - focus on activation, expansion, and helping existing/trial users get more value, not pure cold discovery. Target tactical, implementation-focused engineering leaders (Head of Engineering, VP Engineering, Developer Experience Lead, Platform Lead, Engineering Productivity), NOT strategic execs. Be concrete, specific, and opinionated about developer tools and engineering workflows. Avoid strategic/vague language. Assume the reader is smart and busy. Max 90 words per email. No hype, no pleasantries like 'hope you're well'. When mentioning competitors, explain how the product would be evaluated against them and what tradeoffs the persona would care about (speed vs accuracy, local vs cloud, snippets vs full repo context, etc.). CTAs must be value-driven comparisons or insights with tradeoffs, NOT generic meeting requests like 'would you be open to a call'.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            content = message.content[0].text
            return parse_email_sequence(content, greeting)
        except Exception as e:
            return {"error": f"Anthropic API error: {str(e)}"}
    
    return {"error": f"Unknown provider: {provider}"}


def parse_email_sequence(content: str, greeting: str) -> Dict[str, str]:
    """Parse email sequence from LLM response."""
    result = {
        "email1_subject": None,
        "email1_body": None,
        "email2_subject": None,
        "email2_body": None,
        "email3_subject": None,
        "email3_body": None,
        "linkedin_message": None
    }
    
    lines = content.split('\n')
    current_key = None
    current_value = []
    
    for line in lines:
        line = line.strip()
        if line.startswith('EMAIL1_SUBJECT:') or line.startswith('EMAIL2_SUBJECT:') or line.startswith('EMAIL3_SUBJECT:') or line.startswith('LINKEDIN_MESSAGE:'):
            # Save previous value
            if current_key:
                result[current_key] = '\n'.join(current_value).strip()
            
            # Start new key
            parts = line.split(':', 1)
            key_name = parts[0].lower().replace('_', '_')
            result[key_name] = parts[1].strip() if len(parts) > 1 else ""
            current_key = key_name
            current_value = []
        elif line.startswith('EMAIL1_BODY:') or line.startswith('EMAIL2_BODY:') or line.startswith('EMAIL3_BODY:'):
            # Save previous value
            if current_key:
                result[current_key] = '\n'.join(current_value).strip()
            
            # Start new key
            parts = line.split(':', 1)
            key_name = parts[0].lower().replace('_', '_')
            current_key = key_name
            current_value = [parts[1].strip()] if len(parts) > 1 and parts[1].strip() else []
        elif current_key and line:
            current_value.append(line)
    
    # Save last value
    if current_key:
        result[current_key] = '\n'.join(current_value).strip()
    
    # Replace [First Name] with actual greeting if we have it
    for key in result:
        if result[key] and '[First Name]' in result[key]:
            result[key] = result[key].replace('[First Name]', greeting)
    
    return result
