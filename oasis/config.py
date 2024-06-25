import os
from dotenv import load_dotenv

# 現在の作業ディレクトリの.envファイルを読み込む
load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))

class Config:
    AUTH_USER = os.getenv('AUTH_USER')
    AUTH_PASS = os.getenv('AUTH_PASS')
    BASE_URL = os.getenv('BASE_URL')
    LLM_MODEL = os.getenv('LLM_MODEL', 'gemini/gemini-1.5-pro-latest')  # デフォルトモデル
    END_POINT_URL = f"{BASE_URL}/wp-json/wp/v2/posts/"
    MEDIA_ENDPOINT = f"{BASE_URL}/wp-json/wp/v2/media"
    
    os.environ["GEMINI_API_KEY"] = os.getenv('GEMINI_API_KEY') or "YOUR_DEFAULT_API_KEY_HERE"