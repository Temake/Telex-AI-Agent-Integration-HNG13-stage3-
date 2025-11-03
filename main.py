import os
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json

import httpx
import google.generativeai as genai
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

app = FastAPI(
    title="CompetiScope Agent",
    description="Intelligent Competitor Intelligence Agent",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cache: Dict[str, Dict] = {}
CACHE_TTL = 3600

class CompanyAnalysisRequest(BaseModel):
    company: str = Field(..., description="Company name to analyze")
    market: Optional[str] = Field(None, description="Market/industry sector")
    focus_areas: Optional[List[str]] = Field(None, description="Specific areas to focus on")

class CompetitorIntelligence(BaseModel):
    company: str
    analysis_summary: str
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]
    market_position: str
    recommendations: List[str]
    confidence_score: int
    data_sources: List[str]

class TelexWebhookData(BaseModel):
    content: str
    channel_id: str
    user_id: str
    timestamp: str

# Data collection functions
async def get_company_basic_info(company_name: str) -> Dict[str, Any]:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            search_query = f"{company_name} company information"
            
            basic_info = {
                "name": company_name,
                "industry": "Technology",
                "founded": "Unknown",
                "headquarters": "Unknown",
                "employees": "Unknown",
                "description": f"Information about {company_name}",
                "source": "public_data"
            }
            
            return basic_info
    except Exception as e:
        logger.error(f"Error fetching company info: {e}")
        return {"name": company_name, "error": "Could not fetch basic info"}

async def get_recent_news(company_name: str, days: int = 30) -> List[Dict[str, Any]]:
    try:
        news_items = [
            {
                "title": f"Recent developments at {company_name}",
                "summary": f"Latest news and updates about {company_name}",
                "sentiment": "neutral",
                "date": datetime.now().isoformat(),
                "source": "news_simulation"
            }
        ]
        return news_items
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return []

async def get_market_data(company_name: str) -> Dict[str, Any]:
    try:
        market_data = {
            "market_cap": "Unknown",
            "stock_price": "Unknown",
            "revenue": "Unknown",
            "market_share": "Unknown",
            "growth_rate": "Unknown",
            "source": "market_simulation"
        }
        return market_data
    except Exception as e:
        logger.error(f"Error fetching market data: {e}")
        return {"error": "Could not fetch market data"}

async def analyze_with_ai(company_data: Dict[str, Any], focus_areas: Optional[List[str]] = None) -> Dict[str, Any]:
    try:
        prompt = f"""
        You are CompetiScope, an expert competitive intelligence analyst. Analyze the following company data and provide comprehensive competitive intelligence.

        Company Data:
        {json.dumps(company_data, indent=2)}

        Focus Areas: {focus_areas or ['comprehensive analysis']}

        Provide analysis in the following JSON format:
        {{
            "analysis_summary": "2-3 sentence executive summary of key competitive insights",
            "strengths": ["strength1", "strength2", "strength3"],
            "weaknesses": ["weakness1", "weakness2", "weakness3"],
            "opportunities": ["opportunity1", "opportunity2", "opportunity3"],
            "threats": ["threat1", "threat2", "threat3"],
            "market_position": "Analysis of current market positioning and competitive stance",
            "recommendations": ["actionable recommendation 1", "actionable recommendation 2", "actionable recommendation 3"],
            "confidence_score": 85
        }}

        Be specific, actionable, and business-focused. Base insights on the provided data but also use your knowledge about the industry and market dynamics.
        """

        response = model.generate_content(prompt)
        ai_analysis = json.loads(response.text.strip())
        return ai_analysis
        
    except json.JSONDecodeError:
        logger.error("Failed to parse AI response as JSON")
        return {
            "analysis_summary": f"Basic analysis of {company_data.get('basic_info', {}).get('name', 'company')} based on available data.",
            "strengths": ["Market presence", "Brand recognition", "Innovation capability"],
            "weaknesses": ["Limited data available", "Market competition", "Economic sensitivity"],
            "opportunities": ["Digital transformation", "Market expansion", "Strategic partnerships"],
            "threats": ["Economic uncertainty", "Competitive pressure", "Regulatory changes"],
            "market_position": "Competitive position requires further analysis with more comprehensive data.",
            "recommendations": ["Conduct deeper market research", "Monitor competitor activities", "Focus on differentiation"],
            "confidence_score": 60
        }
    except Exception as e:
        logger.error(f"Error in AI analysis: {e}")
        raise HTTPException(status_code=500, detail="AI analysis failed")

def is_cache_valid(cache_entry: Dict) -> bool:
    if not cache_entry or 'timestamp' not in cache_entry:
        return False
    
    cache_time = datetime.fromisoformat(cache_entry['timestamp'])
    return datetime.now() - cache_time < timedelta(seconds=CACHE_TTL)

async def get_comprehensive_analysis(company: str, market: Optional[str] = None, focus_areas: Optional[List[str]] = None) -> CompetitorIntelligence:
    cache_key = f"{company}_{market}_{'-'.join(focus_areas or [])}"
    if cache_key in cache and is_cache_valid(cache[cache_key]):
        logger.info(f"Returning cached analysis for {company}")
        return CompetitorIntelligence(**cache[cache_key]['data'])
    
    logger.info(f"Generating fresh analysis for {company}")
    
    try:
        tasks = [
            get_company_basic_info(company),
            get_recent_news(company),
            get_market_data(company)
        ]
        
        basic_info, news_data, market_data = await asyncio.gather(*tasks)
        
        comprehensive_data = {
            "basic_info": basic_info,
            "recent_news": news_data,
            "market_data": market_data,
            "analysis_request": {
                "company": company,
                "market": market,
                "focus_areas": focus_areas
            }
        }
        
        ai_insights = await analyze_with_ai(comprehensive_data, focus_areas)
        
        result = CompetitorIntelligence(
            company=company,
            analysis_summary=ai_insights.get("analysis_summary", ""),
            strengths=ai_insights.get("strengths", []),
            weaknesses=ai_insights.get("weaknesses", []),
            opportunities=ai_insights.get("opportunities", []),
            threats=ai_insights.get("threats", []),
            market_position=ai_insights.get("market_position", ""),
            recommendations=ai_insights.get("recommendations", []),
            confidence_score=ai_insights.get("confidence_score", 70),
            data_sources=["company_data", "news_analysis", "market_data", "ai_analysis"]
        )
        
        cache[cache_key] = {
            "data": result.dict(),
            "timestamp": datetime.now().isoformat()
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Error in comprehensive analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/")
async def root():
    return {
        "message": "CompetiScope Agent is running!",
        "version": "1.0.0",
        "status": "healthy",
        "capabilities": [
            "competitor_analysis",
            "market_intelligence",
            "swot_analysis",
            "telex_integration"
        ]
    }

@app.post("/analyze", response_model=CompetitorIntelligence)
async def analyze_competitor(request: CompanyAnalysisRequest):
    logger.info(f"Analyzing competitor: {request.company}")
    
    if not request.company.strip():
        raise HTTPException(status_code=400, detail="Company name is required")
    
    try:
        result = await get_comprehensive_analysis(
            company=request.company,
            market=request.market,
            focus_areas=request.focus_areas
        )
        
        logger.info(f"Analysis completed for {request.company}")
        return result
        
    except Exception as e:
        logger.error(f"Analysis failed for {request.company}: {e}")
        raise HTTPException(status_code=500, detail="Analysis failed")

@app.post("/webhook/telex")
async def telex_webhook(request: Request):
    try:
        data = await request.json()
        
        content = data.get("content", "").strip()
        channel_id = data.get("channel_id", "")
        user_id = data.get("user_id", "")
        
        logger.info(f"Received Telex message: {content}")
        
        if content.lower().startswith(("analyze", "check", "research")):
            parts = content.split(" ", 1)
            if len(parts) > 1:
                company_name = parts[1].strip()
                
                try:
                    analysis = await get_comprehensive_analysis(company_name)
                    
                    response_text = f"""
🔍 **CompetiScope Analysis: {analysis.company}**

📊 **Summary**: {analysis.analysis_summary}

💪 **Strengths**:
{chr(10).join([f"• {s}" for s in analysis.strengths[:3]])}

⚠️ **Weaknesses**:
{chr(10).join([f"• {w}" for w in analysis.weaknesses[:3]])}

🚀 **Key Opportunities**:
{chr(10).join([f"• {o}" for o in analysis.opportunities[:3]])}

💡 **Recommendations**:
{chr(10).join([f"• {r}" for r in analysis.recommendations[:2]])}

📈 **Confidence Score**: {analysis.confidence_score}%
                    """.strip()
                    
                    return {
                        "response": response_text,
                        "channel_id": channel_id,
                        "user_id": user_id
                    }
                    
                except Exception as e:
                    return {
                        "response": f"Sorry, I couldn't analyze {company_name}. Please try again with a different company name.",
                        "channel_id": channel_id,
                        "error": str(e)
                    }
            else:
                return {
                    "response": "Please specify a company name to analyze. Example: 'analyze Apple' or 'research Tesla'",
                    "channel_id": channel_id
                }
        else:
            return {
                "response": "Hi! I'm CompetiScope 🔍 I can analyze competitors for you. Try: 'analyze [company name]'",
                "channel_id": channel_id
            }
            
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return {
            "response": "Sorry, I encountered an error. Please try again.",
            "error": str(e)
        }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "cache_size": len(cache),
        "gemini_configured": bool(os.getenv("GEMINI_API_KEY")),
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"🚀 Starting CompetiScope Agent on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
