# 🤖 LLM-Powered Chatbot with FastAPI and SQL Integration

A modern chatbot application that processes natural language queries about customer data using LLM (Groq) and converts them to SQL queries for database retrieval.

## 🌟 Features

- **Natural Language Processing**: Ask questions in plain English about customer data
- **LLM Integration**: Uses Groq's Llama 3.1 model for SQL query generation
- **FastAPI Backend**: Modern, fast, and well-documented API
- **React Frontend**: Clean, responsive UI with real-time query processing
- **SQLite Database**: Lightweight database with sample customer data
- **Error Handling**: Comprehensive error handling and logging

## 🏗️ Tech Stack

- **Backend**: FastAPI, Python 3.8+
- **Frontend**: React 18, CSS3
- **Database**: SQLite3
- **LLM**: Groq API (Llama 3.1)
- **Additional**: python-dotenv, uvicorn, logging

## 📋 Prerequisites

1. **Python 3.8+** installed on your system
2. **Node.js 16+** and npm for the React frontend
3. **Groq API Key**

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd llm-chatbot
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env
# Edit .env and add your GROQ_API_KEY
```

### 3. Initialize Database

```bash
# Run the database initialization script
python database.py
```

This will create a SQLite database with sample customer data.

### 4. Start the Backend Server

```bash
# Start FastAPI server
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### 5. Frontend Setup

```bash
# In a new terminal, navigate to frontend directory
mkdir frontend
cd frontend

# Initialize React app
npx create-react-app <your-app-name>.

# Install dependencies
npm install

# Start the React development server
npm start
```

The frontend will be available at `http://localhost:3000`

## 📊 Database Schema

The application uses a simple customer database:

```sql
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    gender TEXT NOT NULL CHECK (gender IN ('Male', 'Female')),
    location TEXT NOT NULL
);
```

## 🔍 Example Queries

Try these natural language queries:

- "Show me all female customers"
- "Find customers from Mumbai"
- "Show male customers from Pune"
- "List all customers from Singapore"
- "Find customers named Shubh"
- "How many customers are there?"
- "Show customers from Mumbai and Pune"

## 🛠️ API Endpoints

### POST `/query`
Process natural language query and return SQL results.

**Request Body:**
```json
{
    "query": "Show me all female customers from Mumbai"
}
```

**Response:**
```json
{
    "results": [...],
    "generated_sql": "SELECT * FROM customers WHERE gender = 'Female' AND location = 'Mumbai'",
    "message": "Found 3 result(s)"
}
```

### GET `/customers`
Get all customers (for testing purposes).

## 🔒 Security Features

- **SQL Injection Prevention**: Only SELECT queries allowed
- **Input Validation**: Query sanitization and validation
- **Error Handling**: Proper error messages without exposing internals
- **CORS Configuration**: Restricted to frontend origin

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Groq** for providing the LLM API
- **FastAPI** for the excellent Python web framework  
- **React** for the frontend framework
- **SQLite** for the lightweight database solution

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the logs for error details
3. Open an issue on GitHub with:
   - Error message
   - Steps to reproduce
   - Your environment details
