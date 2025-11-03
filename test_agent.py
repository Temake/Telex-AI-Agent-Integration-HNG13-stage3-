


import asyncio
import json
import httpx
from datetime import datetime

async def test_agent():
    """Test the CompetiScope agent locally"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Testing CompetiScope Agent...")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        
        # Test 1: Health check
        print("1. Testing health check...")
        try:
            response = await client.get(f"{base_url}/")
            print(f"✅ Health check: {response.status_code}")
            print(f"   Response: {response.json()}")
        except Exception as e:
            print(f"❌ Health check failed: {e}")
        
        print()
        
        # Test 2: Basic competitor analysis
        print("2. Testing competitor analysis...")
        test_data = {
            "company": "Apple Inc",
            "market": "technology",
            "focus_areas": ["strengths", "opportunities"]
        }
        
        try:
            response = await client.post(
                f"{base_url}/analyze",
                json=test_data,
                timeout=30.0
            )
            print(f"✅ Analysis request: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   Company: {result['company']}")
                print(f"   Summary: {result['analysis_summary'][:100]}...")
                print(f"   Confidence: {result['confidence_score']}%")
                print(f"   Strengths: {len(result['strengths'])} items")
                print(f"   Recommendations: {len(result['recommendations'])} items")
            else:
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
        
        print()
        
        # Test 3: Telex webhook simulation
        print("3. Testing Telex webhook...")
        webhook_data = {
            "content": "analyze Microsoft",
            "channel_id": "test-channel-123",
            "user_id": "test-user-456",
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            response = await client.post(
                f"{base_url}/webhook/telex",
                json=webhook_data,
                timeout=30.0
            )
            print(f"✅ Webhook test: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   Response length: {len(result.get('response', ''))} chars")
                print(f"   Channel ID: {result.get('channel_id')}")
            else:
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Webhook test failed: {e}")
    
    print("\n🏁 Testing completed!")

if __name__ == "__main__":
    print("Make sure the server is running with: uvicorn main:app --reload")
    print("Starting tests in 3 seconds...")
    
    import time
    time.sleep(3)
    
    asyncio.run(test_agent())