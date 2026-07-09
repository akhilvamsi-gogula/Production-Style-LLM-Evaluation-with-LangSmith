import os
from pathlib import Path
from dotenv import load_dotenv

def load_project_env():
    # Force dotenv to load the .env file located explicitly next to this _env.py file
    env_path = Path(__file__).resolve().parent / ".env"
    
    # Passing the exact path guarantees it loads no matter where you execute the script from
    load_dotenv(dotenv_path=env_path)
    
    if not os.getenv("LANGCHAIN_API_KEY"):
        print("[WARNING] LANGCHAIN_API_KEY is not set in .env")
    if not os.getenv("GROQ_API_KEY"):
        print("[WARNING] GROQ_API_KEY is not set in .env")
        
    os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
    os.environ.setdefault("LANGCHAIN_PROJECT", "langsmith-evaluation-prototype")