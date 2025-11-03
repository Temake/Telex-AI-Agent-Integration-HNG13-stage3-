# CompetiScope - Intelligent Competitor Intelligence Agent

CompetiScope is an AI-powered competitor intelligence agent that delivers instant business insights by analyzing company data and providing actionable competitive intelligence.

## Features

- **Real-time Company Analysis**: Fetches company information from multiple sources
- **AI-Powered Insights**: Uses Google Gemini API for intelligent analysis
- **SWOT Analysis**: Provides strengths, weaknesses, opportunities, and threats
- **Market Positioning**: Analyzes competitive positioning and market trends
- **News & Sentiment Analysis**: Tracks recent news and market sentiment
- **Telex.im Integration**: Seamlessly integrates with Telex.im platform

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -e .
   ```

2. **Set Environment Variables**:
   Create a `.env` file:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   NEWS_API_KEY=your_news_api_key_here (optional)
   ```

3. **Run the Agent**:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

4. **Test the Agent**:
   ```bash
   curl -X POST "http://localhost:8000/analyze" \
        -H "Content-Type: application/json" \
        -d '{"company": "Apple Inc", "market": "technology"}'
   ```

## API Endpoints

### POST /analyze
Analyzes a competitor and returns comprehensive intelligence report.

**Request Body**:
```json
{
  "company": "Company Name",
  "market": "industry sector (optional)",
  "focus_areas": ["strengths", "weaknesses", "opportunities"] // optional
}
```

**Response**:
```json
{
  "company": "Company Name",
  "analysis_summary": "Executive summary of competitive intelligence",
  "strengths": ["Key strength 1", "Key strength 2"],
  "weaknesses": ["Weakness 1", "Weakness 2"],
  "opportunities": ["Opportunity 1", "Opportunity 2"],
  "threats": ["Threat 1", "Threat 2"],
  "market_position": "Current market positioning analysis",
  "recommendations": ["Action 1", "Action 2"],
  "confidence_score": 85,
  "data_sources": ["source1", "source2"]
}
```

### POST /webhook/telex
Telex.im webhook endpoint for A2A protocol integration.

## Integration with Telex.im

The agent integrates with Telex.im using the A2A protocol. Users can interact with CompetiScope directly through Telex chat by sending company names for analysis.

### Example Usage in Telex:
```
User: Analyze Tesla as a competitor
CompetiScope: [Provides comprehensive competitive intelligence report]
```

## Architecture

- **FastAPI**: Web framework for API endpoints
- **Google Gemini**: AI model for intelligent analysis
- **Multi-source Data**: Aggregates data from various public APIs
- **Caching**: Simple in-memory caching for performance
- **Error Handling**: Robust error handling and validation

## Development

The agent is designed to be:
- **Simple**: Easy to understand and modify
- **Scalable**: Can be extended with additional data sources
- **Reliable**: Comprehensive error handling
- **Fast**: Efficient data processing and caching

## License

MIT License
