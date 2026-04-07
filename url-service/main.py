import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Import our custom logic modules
from snowflake import SnowflakeGenerator
from converter import Base62Converter
from database import save_url, get_long_url

# 1. Initialization
load_dotenv()
app = FastAPI(title="Distributed URL Shortener")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, you'd specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Snowflake with unique Machine ID from .env
MACHINE_ID = int(os.getenv("MACHINE_ID", 1))
snowflake = SnowflakeGenerator(machine_id=MACHINE_ID)

# 2. Data Models
class URLRequest(BaseModel):
    long_url: str

# 3. API Endpoints
PUBLIC_URL = os.getenv("PUBLIC_URL", "http://localhost:8000/")

@app.post("/shorten")
async def shorten_url(request: URLRequest):
    try:
        # 1. Generate ID
        snowflake_id = snowflake.generate_id()
        
        # 2. Encode to Base62
        short_code = Base62Converter.encode(snowflake_id)
        
        # 3. Save to Supabase
        save_url(snowflake_id, short_code, request.long_url)
        
        # 4. Return the clean URL using the environment variable
        return {
            "short_code": short_code,
            "short_url": f"{PUBLIC_URL}{short_code}",
            "long_url": request.long_url
        }
    except Exception as e:
        print(f"CRITICAL CRASH REASON: {e}") 
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/{short_code}")
async def redirect_to_long_url(short_code: str):
    """
    Step 1: Lookup short_code in Supabase.
    Step 2: If found, perform 302 redirect.
    """
    long_url = get_long_url(short_code)
    
    if long_url:
        # Perform temporary redirect to maintain analytics [cite: 34, 77]
        return RedirectResponse(url=long_url, status_code=302)
    
    raise HTTPException(status_code=404, detail="Short URL not found")