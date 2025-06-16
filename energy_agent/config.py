import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv()

class Config:
    # OpenRouter Configuration
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"
    
    # Modo Energy API Configuration
    MODO_API_KEY = os.getenv("MODO_API_KEY")
    MODO_API_BASE = "https://api.modo.energy"
    
    # Model Configuration
    DEFAULT_MODEL = "qwen/qwen-2-72b-instruct"
    MODEL = "qwen/qwen-2.5-72b-instruct:free"
    
    # Data Directories
    DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    CACHE_DIR = os.path.join(DATA_DIR, "cache")
    
    # Create directories if they don't exist
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)


# Initialize config
config = Config()
