#!/usr/bin/env python3
"""
CLI entry point for Account Brief Generator.
"""

import argparse
import re
import sys
from pathlib import Path

from src.renderer import render_account_brief


def sanitize_filename(company: str) -> str:
    """
    Sanitize company name for use as a filename.
    
    Args:
        company: Company name
        
    Returns:
        Sanitized filename-safe string
    """
    # Replace spaces and special characters with hyphens
    sanitized = re.sub(r'[^\w\s-]', '', company)
    sanitized = re.sub(r'[-\s]+', '-', sanitized)
    # Remove leading/trailing hyphens
    sanitized = sanitized.strip('-')
    # Fallback if empty
    return sanitized if sanitized else "company"


def get_next_version(company_dir: Path, company_name: str) -> int:
    """
    Get the next version number for a company's account briefs.
    
    Args:
        company_dir: Path to the company's directory
        company_name: Sanitized company name
        
    Returns:
        Next version number (1 if no existing versions)
    """
    if not company_dir.exists():
        return 1
    
    # Find all existing version files
    pattern = f"{company_name}-v*.md"
    existing_files = list(company_dir.glob(pattern))
    
    if not existing_files:
        return 1
    
    # Extract version numbers
    versions = []
    version_pattern = re.compile(rf"{re.escape(company_name)}-v(\d+)\.md")
    
    for file in existing_files:
        match = version_pattern.match(file.name)
        if match:
            versions.append(int(match.group(1)))
    
    if not versions:
        return 1
    
    return max(versions) + 1


def get_output_path(company: str) -> Path:
    """
    Get the output path for a company's account brief with versioning.
    
    Args:
        company: Company name
        
    Returns:
        Path object for the output file
    """
    outputs_dir = Path("outputs")
    outputs_dir.mkdir(exist_ok=True)
    
    # Sanitize company name
    sanitized_company = sanitize_filename(company)
    
    # Create company-specific directory
    company_dir = outputs_dir / sanitized_company
    company_dir.mkdir(exist_ok=True)
    
    # Get next version number
    version = get_next_version(company_dir, sanitized_company)
    
    # Create filename with version
    filename = f"{sanitized_company}-v{version}.md"
    
    return company_dir / filename


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate a structured markdown account brief",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --company "Acme Corp" --persona "CTO" --competitor "VendorX"
  python main.py -c "TechStart Inc" -p "VP Engineering" -co "CompetitorY"
        """
    )
    
    parser.add_argument(
        "--company", "-c",
        type=str,
        required=True,
        help="Company name"
    )
    
    parser.add_argument(
        "--persona", "-p",
        type=str,
        required=True,
        help="Target persona (e.g., Head of Engineering, VP Engineering, Developer Experience Lead, Platform Lead, Engineering Productivity)"
    )
    
    parser.add_argument(
        "--competitor", "-co",
        type=str,
        default="Unknown",
        help="Competitor name(s), comma-separated for multiple (default: Unknown)"
    )
    
    parser.add_argument(
        "--no-research",
        action="store_true",
        help="Skip web research and use template placeholders only"
    )
    
    parser.add_argument(
        "--llm",
        choices=["openai", "anthropic"],
        default=None,
        help="Use LLM to research persona names and enhance content (requires API key in OPENAI_API_KEY or ANTHROPIC_API_KEY env var)"
    )
    
    args = parser.parse_args()
    
    # Parse competitors from comma-separated string
    competitors = [c.strip() for c in args.competitor.split(",")] if args.competitor else ["Unknown"]
    
    try:
        brief = render_account_brief(
            company=args.company,
            persona=args.persona,
            competitors=competitors,
            use_research=not args.no_research,
            use_llm=args.llm is not None,
            llm_provider=args.llm or "openai"
        )
        
        # Get output path with versioning
        output_file = get_output_path(args.company)
        
        # Write to file
        output_file.write_text(brief, encoding='utf-8')
        
        print(f"Account brief saved to: {output_file}", file=sys.stderr)
        
    except Exception as e:
        print(f"Error generating account brief: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
