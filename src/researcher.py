"""
Web research module for gathering account information.
"""

import re
from typing import Dict, List, Optional

try:
    from duckduckgo_search import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False


def search_web(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Search the web using DuckDuckGo (no API key required).
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
        
    Returns:
        List of dictionaries with 'title', 'url', and 'body' keys
    """
    if not DDGS_AVAILABLE:
        return []
    
    try:
        results = []
        with DDGS() as ddgs:
            search_results = ddgs.text(query, max_results=max_results)
            for result in search_results:
                results.append({
                    'title': result.get('title', ''),
                    'url': result.get('href', ''),
                    'body': result.get('body', '')
                })
        return results
    except Exception as e:
        # Try alternative approach if DDGS context manager fails
        try:
            ddgs = DDGS()
            search_results = ddgs.text(query, max_results=max_results)
            results = []
            for result in search_results:
                results.append({
                    'title': result.get('title', ''),
                    'url': result.get('href', ''),
                    'body': result.get('body', '')
                })
            return results
        except Exception as e2:
            print(f"Warning: Web search failed: {e2}", file=__import__('sys').stderr)
            return []


def research_company(company: str) -> Dict[str, any]:
    """
    Research a company and gather relevant information.
    
    Args:
        company: Company name
        
    Returns:
        Dictionary with researched information
    """
    research_data = {
        'recent_news': [],
        'funding_info': None,
        'hiring_trends': None,
        'description': None,
        'all_snippets': []
    }
    
    # Search for recent news
    news_query = f"{company} news 2024"
    research_data['recent_news'] = search_web(news_query, max_results=5)
    
    # Search for funding information
    funding_query = f"{company} funding investment raised"
    funding_results = search_web(funding_query, max_results=3)
    research_data['funding_info'] = funding_results
    
    # Search for company description/about
    desc_query = f"{company} company about"
    desc_results = search_web(desc_query, max_results=3)
    research_data['description'] = desc_results
    
    # Collect all snippets for context
    all_snippets = []
    for result in research_data['recent_news'] + research_data['funding_info'] + research_data['description']:
        if result.get('body'):
            all_snippets.append(result['body'])
    research_data['all_snippets'] = all_snippets
    
    return research_data


def extract_why_now_triggers(company: str, research_data: Dict[str, any]) -> List[str]:
    """
    Extract "why now" triggers from research data.
    
    Args:
        company: Company name
        research_data: Research data dictionary
        
    Returns:
        List of trigger statements
    """
    triggers = []
    snippets = research_data.get('all_snippets', [])
    
    if snippets:
        combined_text = ' '.join(snippets[:5]).lower()  # Use first 5 snippets
        
        # Look for funding keywords
        funding_keywords = ['funding', 'raised', 'investment', 'series', 'funded', 'million', 'billion', '$']
        if any(keyword in combined_text for keyword in funding_keywords):
            triggers.append(f"{company} has recent funding activity indicating growth and investment in new solutions")
        
        # Look for hiring/expansion keywords
        hiring_keywords = ['hiring', 'expanding', 'growing', 'team', 'openings', 'jobs', 'recruiting']
        if any(keyword in combined_text for keyword in hiring_keywords):
            triggers.append(f"Active hiring and team expansion at {company} suggests scaling and infrastructure needs")
        
        # Look for partnership/launch keywords
        launch_keywords = ['launch', 'partnership', 'announces', 'introduces', 'new product', 'release']
        if any(keyword in combined_text for keyword in launch_keywords):
            triggers.append(f"Recent product launches or partnerships at {company} indicate active development")
    
    # Only add generic fallback if no triggers found (avoid generic phrases)
    if not triggers:
        triggers = [
            f"Research {company}'s recent funding rounds, hiring activity, or expansion plans",
            f"Identify recent product launches, partnerships, or strategic initiatives at {company}",
            f"Review {company}'s growth trajectory and infrastructure scaling needs"
        ]
    
    return triggers[:3]  # Return top 3


def get_persona_pain_points(persona: str) -> List[str]:
    """
    Get common pain points for a persona/role.
    
    Args:
        persona: Persona/role name (e.g., "CTO", "VP Engineering")
        
    Returns:
        List of common pain points
    """
    # Generic pain points by role type
    pain_points_map = {
        'cto': [
            "Balancing technical debt with innovation and new feature development",
            "Scaling infrastructure and engineering teams while maintaining code quality",
            "Ensuring security and compliance without slowing down development velocity",
            "Managing vendor relationships and tool sprawl across engineering stack",
            "Attracting and retaining top engineering talent in competitive market"
        ],
        'vp engineering': [
            "Optimizing team productivity and delivery velocity",
            "Managing technical debt and architectural decisions at scale",
            "Balancing feature development with infrastructure improvements",
            "Cross-team collaboration and communication challenges",
            "Tool and process standardization across engineering teams"
        ],
        'vp sales': [
            "Accelerating sales cycle and improving win rates",
            "Forecasting accuracy and pipeline management",
            "Sales team productivity and quota attainment",
            "Competitive differentiation and positioning",
            "Sales and marketing alignment"
        ]
    }
    
    # Try to match persona (case-insensitive)
    persona_lower = persona.lower()
    for key, points in pain_points_map.items():
        if key in persona_lower:
            return points
    
    # Default generic pain points
    return [
        f"Common {persona} challenges around strategic decision-making",
        f"{persona} pain points related to team and resource management",
        f"Budget and ROI concerns facing {persona}s",
        f"{persona} frustrations with current tools and processes",
        f"Business impact of unresolved challenges for {persona} role"
    ]


def generate_discovery_questions(persona: str, company: str, competitors: List[str]) -> List[str]:
    """
    Generate discovery questions based on persona and context.
    
    Args:
        persona: Target persona
        company: Company name
        competitors: List of competitors
        
    Returns:
        List of 5 discovery questions
    """
    competitors_text = ", ".join(competitors) if competitors else "your current solutions"
    
    questions = [
        f"What are the biggest challenges you're facing as {persona} at {company} right now?",
        f"How do you currently handle [key process/need]? What works well and what doesn't?",
        f"What would need to happen for this to become a priority for your team?",
        f"Have you evaluated {competitors_text}? What were your thoughts on those?",
        f"What's your timeline for addressing these challenges? Who else is involved in the decision?"
    ]
    
    return questions
