"""
Configuration and utility functions for CompetiScope Agent
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class Config:
    """Application configuration"""
    gemini_api_key: str
    news_api_key: Optional[str] = None
    alpha_vantage_key: Optional[str] = None
    host: str = "0.0.0.0"
    port: int = 8000
    cache_ttl: int = 3600
    telex_webhook_secret: Optional[str] = None

def get_config() -> Config:
    """Load configuration from environment variables"""
    return Config(
        gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
        news_api_key=os.getenv("NEWS_API_KEY"),
        alpha_vantage_key=os.getenv("ALPHA_VANTAGE_API_KEY"),
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        cache_ttl=int(os.getenv("CACHE_TTL", 3600)),
        telex_webhook_secret=os.getenv("TELEX_WEBHOOK_SECRET")
    )

def format_currency(amount: float) -> str:
    """Format currency amounts"""
    if amount >= 1_000_000_000:
        return f"${amount/1_000_000_000:.1f}B"
    elif amount >= 1_000_000:
        return f"${amount/1_000_000:.1f}M"
    elif amount >= 1_000:
        return f"${amount/1_000:.1f}K"
    else:
        return f"${amount:.2f}"

def extract_company_name(text: str) -> Optional[str]:
    """Extract company name from natural language text"""
    # Simple extraction - can be enhanced with NLP
    text = text.strip().lower()
    
    # Remove common words
    remove_words = ["analyze", "check", "research", "tell", "me", "about", "company", "competitor"]
    words = text.split()
    filtered_words = [w for w in words if w not in remove_words]
    
    if filtered_words:
        return " ".join(filtered_words).title()
    return None

def validate_api_keys() -> Dict[str, bool]:
    """Validate that required API keys are present"""
    config = get_config()
    return {
        "gemini": bool(config.gemini_api_key),
        "news_api": bool(config.news_api_key),
        "alpha_vantage": bool(config.alpha_vantage_key)
    }