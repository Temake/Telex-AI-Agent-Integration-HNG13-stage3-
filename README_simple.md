# CompetiScope Agent

Intelligent competitor intelligence agent that delivers instant business insights using AI.

## Features

- Real-time competitor analysis
- SWOT analysis (Strengths, Weaknesses, Opportunities, Threats)
- Market positioning insights
- Actionable recommendations
- Telex.im integration
- Simple caching for performance

## Quick Start

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   GEMINI_API_KEY=your_gemini_api_key_here
   PORT=8000
   ```

4. Run the application:
   ```bash
   python main.py
   ```

## API Endpoints

- `GET /` - Health check
- `POST /analyze` - Analyze a competitor
- `POST /webhook/telex` - Telex.im webhook
- `GET /health` - Detailed health check

## Usage with Telex.im

Send messages like:
- "analyze Apple"
- "research Tesla"
- "check Microsoft"

## Deployment

Deploy to Render, Railway, or any Python hosting platform.

## Environment Variables

- `GEMINI_API_KEY` - Your Google Gemini API key
- `PORT` - Server port (default: 8000)
- `HOST` - Server host (default: 0.0.0.0)