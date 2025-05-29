from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os
import logging
from groq import Groq
from dotenv import load_dotenv
import json
import re


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(title="LLM-Powered Chatbot")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initialize Groq
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Database configuration
DATABASE_PATH = "customers.db"

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    results: list
    generated_sql: str
    message: str

def init_database():
    """Initialize the database with sample data"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Customer table creation
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            gender TEXT NOT NULL,
            location TEXT NOT NULL
        )
    """)
    
    cursor.execute("SELECT COUNT(*) FROM customers")
    if cursor.fetchone()[0] == 0:
        # Insert sample data
        sample_customers = [
        ("Sneh Jain", "Male", "Mumbai"),
        ("Smit Jain", "Male", "Mumbai"),
        ("Khushi Jain", "Female", "Germany"),
        ("Sejal Jain", "Female", "Pune"),
        ("Shubh Jain", "Male", "Mumbai"),
        ("Isha Jain", "Female", "Pune"),
        ("Sanskar Jain", "Male", "Pune"),
        ("Aayush Jain", "Male", "Singapore"),
        ("Disha Jain", "Female", "Indore"),
        ("Bhumi Jain", "Female", "Mumbai"),
    ]
        
        cursor.executemany(
            "INSERT INTO customers (name, gender, location) VALUES (?, ?, ?)",
            sample_customers
        )
        conn.commit()
        logger.info("Database initialized with sample data")
    
    conn.close()

def get_llm_response(user_query: str) -> str:
    """Generate SQL query using Groq LLM"""
    system_prompt = """You are a SQL query generator. Given a natural language query about customers, generate a valid SQLite query.

Database schema:
- Table: customers
- Columns: customer_id (INTEGER PRIMARY KEY), name (TEXT), gender (TEXT), location (TEXT)

Rules:
1. Only generate SELECT queries for safety
2. Use proper SQL syntax for SQLite
3. Common locations: Mumbai, Pune, Indore, Germany, Singapore
4. Return only the SQL query
5. Use LIKE for partial text matches
6. Gender values are 'Male' or 'Female' (case-sensitive)

Examples:
- "Show me all female customers" → SELECT * FROM customers WHERE gender = 'Female'
- "Find customers from Mumbai" → SELECT * FROM customers WHERE location = 'Mumbai'
- "Show Female customers from Pune" → SELECT * FROM customers WHERE gender = 'Female' AND location = 'Pune'
"""
    
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            max_tokens=150,
        )
        
        sql_query = response.choices[0].message.content.strip()
        logger.info(f"Generated SQL: {sql_query}")
        return sql_query
        
    except Exception as e:
        logger.error(f"Error generating SQL with Groq: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate SQL query")

def execute_sql_query(sql_query: str) -> list:
    """Execute SQL query and return results"""
    if not sql_query.strip().upper().startswith('SELECT'):
        raise HTTPException(status_code=400, detail="Only SELECT queries are allowed")
    
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute(sql_query)
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        
        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))
        
        conn.close()
        logger.info(f"Query executed successfully, returned {len(results)} rows")
        return results
        
    except sqlite3.Error as e:
        logger.error(f"SQL execution error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"SQL execution error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database query failed")

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_database()

@app.get("/")
async def root():
    return {"message": "LLM-Powered Chatbot API is running....."}

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process natural language query and return SQL results"""
    try:
        logger.info(f"Incoming query: {request.query}")
        
        sql_query = get_llm_response(request.query)
        
        results = execute_sql_query(sql_query)
        
        message = f"Found {len(results)} result(s)" if results else "No results found"
        
        return QueryResponse(
            results=results,
            generated_sql=sql_query,
            message=message
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in process_query: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/customers")
async def get_all_customers():
    """Get all customers for testing"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM customers")
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        
        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))
        
        conn.close()
        return {"customers": results}
        
    except Exception as e:
        logger.error(f"Error fetching customers: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch customers")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)