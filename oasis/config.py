import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    AUTH_USER = os.getenv('AUTH_USER')
    AUTH_PASS = os.getenv('AUTH_PASS')
    BASE_URL = os.getenv('BASE_URL')
    LLM_MODEL = os.getenv('LLM_MODEL', 'gemini/gemini-1.5-pro-latest')  # デフォルトモデル
    END_POINT_URL = f"{BASE_URL}/wp-json/wp/v2/posts/"
    MEDIA_ENDPOINT = f"{BASE_URL}/wp-json/wp/v2/media"
    
    os.environ["GEMINI_API_KEY"] = os.getenv('GEMINI_API_KEY')
