"""
Markdown renderer for account brief generation.
"""

from datetime import datetime
from typing import List, Optional

from .prompts import format_competitors_display
from .researcher import research_company, extract_why_now_triggers, get_persona_pain_points, generate_discovery_questions
from .llm_researcher import enhance_brief_with_llm, generate_email_sequence_with_llm


def render_account_brief(company: str, persona: str, competitors: List[str], 
                        use_research: bool = True, use_llm: bool = False, llm_provider: str = "openai") -> str:
    """
    Render a structured markdown account brief.
    
    Args:
        company: The company name
        persona: The target persona
        competitors: List of competitor names
        use_research: Whether to use web research to populate the brief
        use_llm: Whether to use LLM to research persona names and enhance content
        llm_provider: LLM provider ("openai" or "anthropic")
        
    Returns:
        A formatted markdown string containing the account brief
    """
    competitors_display = format_competitors_display(competitors)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # LLM enhancement (optional)
    llm_data = {}
    persona_name = None
    company_description = None
    company_employees = None
    company_engineering_team = None
    company_funding = None
    company_revenue = None
    company_headquarters = None
    company_recent_news = None
    company_tech_stack = None
    company_differentiators = None
    email_sequences = {}
    
    if use_llm:
        try:
            llm_data = enhance_brief_with_llm(company, persona, competitors, use_persona_research=True, provider=llm_provider)
            persona_name = llm_data.get("persona_name")
            company_description = llm_data.get("company_description")
            company_employees = llm_data.get("company_employees")
            company_engineering_team = llm_data.get("company_engineering_team")
            company_funding = llm_data.get("company_funding")
            company_revenue = llm_data.get("company_revenue")
            company_headquarters = llm_data.get("company_headquarters")
            company_recent_news = llm_data.get("company_recent_news")
            company_tech_stack = llm_data.get("company_tech_stack")
            company_differentiators = llm_data.get("company_differentiators")
            
            # Generate real email sequences (no placeholders) if we have company data
            if company_description or company_recent_news or company_funding:
                company_info_dict = {
                    "description": company_description,
                    "recent_news": company_recent_news,
                    "funding": company_funding,
                    "employees": company_employees,
                    "engineering_team": company_engineering_team
                }
                email_sequences = generate_email_sequence_with_llm(
                    company, persona, persona_name or persona,
                    company_info_dict, competitors,
                    get_persona_pain_points(persona) if use_research else [],
                    provider=llm_provider
                )
        except Exception as e:
            print(f"Warning: LLM research failed: {e}", file=__import__('sys').stderr)
    
    # Research company if enabled
    if use_research:
        research_data = research_company(company)
        why_now_triggers = extract_why_now_triggers(company, research_data)
        pain_points = get_persona_pain_points(persona)
        discovery_questions = generate_discovery_questions(persona, company, competitors)
    else:
        why_now_triggers = [
            f"Research {company}'s recent funding, hiring, or expansion activities",
            f"Identify regulatory changes or market shifts affecting {company}",
            f"Determine timing-related factors that make this a good time to reach out"
        ]
        pain_points = [
            f"[Identify key challenges and pain points specific to the {persona} role]",
            f"[Common frustrations with current solutions or processes]",
            f"[Business impact of unresolved pain points]"
        ]
        discovery_questions = [
            f"[Question 1 - Focused on understanding current state or challenges]",
            f"[Question 2 - Exploring impact and business outcomes]",
            f"[Question 3 - Identifying decision-making process]",
            f"[Question 4 - Understanding competitive landscape or alternatives]",
            f"[Question 5 - Uncovering budget, timeline, or next steps]"
        ]
    
    # Format sections
    why_now_section = "\n".join(f"- {trigger}" for trigger in why_now_triggers)
    pain_points_section = "\n".join(f"- {point}" for point in pain_points)
    questions_section = "\n".join(f"{i+1}. {q}" for i, q in enumerate(discovery_questions))
    
    # Use persona name if found
    persona_display = persona_name if persona_name else persona
    greeting_name = persona_name if persona_name else "[First Name]"
    
    # Use generated emails if available, otherwise use templates
    use_generated_emails = use_llm and email_sequences and "error" not in email_sequences and email_sequences.get("email1_body")
    
    # Build email section content
    if use_generated_emails:
        email_section = f"""
### Email 1: Initial Outreach

**Subject:** {email_sequences.get("email1_subject", f"Quick question for {persona_display} at {company}")}

{email_sequences.get("email1_body", "")}

---

### Email 2: Follow-up (3-5 days later)

**Subject:** {email_sequences.get("email2_subject", f"Re: Quick question for {persona_display} at {company}")}

{email_sequences.get("email2_body", "")}

---

### Email 3: Final Follow-up (5-7 days after Email 2)

**Subject:** {email_sequences.get("email3_subject", f"Re: Quick question for {persona_display} at {company} - Final Follow-up")}

{email_sequences.get("email3_body", "")}

---

## 1 LinkedIn Message

{email_sequences.get("linkedin_message", "")}"""
    else:
        email_section = f"""
### Email 1: Initial Outreach

**Subject:** Quick question for {persona_display} at {company}

Hi {greeting_name},

As {persona} at {company}, I wanted to reach out about how we help similar {persona}s address their key challenges.

[Research {company}'s specific needs and customize this email with relevant value proposition]

Would you be open to a brief 15-minute conversation to explore if there's a fit?

Best regards,
[Your Name]

---

### Email 2: Follow-up (3-5 days later)

**Subject:** Re: Quick question for {persona_display} at {company}

Hi {greeting_name},

Following up on my previous email - I know you're busy, so I'll keep this brief.

[Add specific insight, case study, or resource relevant to {company}'s business]

If it makes sense, happy to schedule a quick call. If not, no worries - I can send over some resources instead.

Best,
[Your Name]

---

### Email 3: Final Follow-up (5-7 days after Email 2)

**Subject:** Re: Quick question for {persona_display} at {company} - Final Follow-up

Hi {greeting_name},

I know this is my last outreach, so I'll keep it brief.

[Add final value proposition specific to {company}'s needs and how you differentiate from {competitors_display}]

If the timing isn't right now, I'd be happy to stay in touch and share relevant insights as they come up. Would that be helpful?

Thanks for your time,
[Your Name]

---

## 1 LinkedIn Message

Hi {greeting_name},

I noticed you're {persona_display} at {company} - [research and add specific comment about {company}].

I've been working with {persona}s at similar companies to help them [specific area relevant to {persona} and {company}'s business model].

Would love to share how we've helped other {persona}s. Open to a quick chat to see if it might be relevant?

Best,
[Your Name]"""
    
    brief = f"""# Account Brief: {company}

## Account Overview

**Company:** {company}
{f"**Description:** {company_description}" if company_description else ""}
**Target Persona:** {persona}{f" ({persona_name})" if persona_name else ""}
**Competitors:** {competitors_display}
{f"**Headquarters:** {company_headquarters}" if company_headquarters else ""}
{f"**Company Size:** {company_employees} employees" if company_employees else ""}
{f"**Engineering Team Size:** {company_engineering_team}" if company_engineering_team else ""}
{f"**Funding:** {company_funding}" if company_funding else ""}
{f"**Revenue/ARR:** {company_revenue}" if company_revenue else ""}
{f"**Technology Stack:** {company_tech_stack}" if company_tech_stack else ""}
{f"**Key Differentiators:** {company_differentiators}" if company_differentiators else ""}

## Why Now Triggers

{why_now_section}

## Persona Pain Points

**Pain Points for {persona}:**
{pain_points_section}

## 5 Discovery Questions

{questions_section}

## 3-Email Outbound Sequence
{email_section}

---

## Objection Handling

### Common Objections & Responses

**Objection 1: "We're not interested right now"**
- Response: [Acknowledge, offer value, keep door open - e.g., "I understand timing might not be right. Would you be open to receiving relevant resources/insights in the meantime?"]

**Objection 2: "We already have a solution"**
- Response: [Acknowledge, differentiate, explore - e.g., "That's great you have something in place. Many {persona}s find value in understanding how we compare to {competitors_display}. Mind if I share a brief comparison?"]

**Objection 3: "We don't have budget"**
- Response: [Reframe, explore priorities, offer alternatives - e.g., "I appreciate the transparency. Often budget depends on priorities. What would need to change for this to become a priority?"]

**Objection 4: "Send me information and I'll review it"**
- Response: [Provide value, but also push for engagement - e.g., "Happy to send materials. Would a 15-minute call be helpful to ensure the info is most relevant to your situation?"]

**Objection 5: "I need to discuss with my team"**
- Response: [Support the process, offer to help, maintain momentum - e.g., "That makes sense. Would it be helpful if I joined that discussion or prepared materials you can share with your team?"]

---

*Generated on {timestamp}*
"""
    return brief
