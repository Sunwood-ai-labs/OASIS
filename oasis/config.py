import os
from dotenv import load_dotenv

# 現在の作業ディレクトリの.envファイルを読み込む
load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))

class Config:
    AUTH_USER = os.getenv('AUTH_USER')
    AUTH_PASS = os.getenv('AUTH_PASS')
    BASE_URL = os.getenv('BASE_URL')
    LLM_MODEL = os.getenv('LLM_MODEL', 'gemini/gemini-1.5-pro-latest')  # デフォルトモデル
    QIITA_TOKEN = os.getenv('QIITA_TOKEN')
    
    # WordPressのエンドポイント
    END_POINT_URL = f"{BASE_URL}/wp-json/wp/v2/posts/" if BASE_URL else None
    MEDIA_ENDPOINT = f"{BASE_URL}/wp-json/wp/v2/media" if BASE_URL else None
    
    # Gemini API キー
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    @classmethod
    def validate(cls):
        """設定の妥当性を検証するメソッド"""
        if not cls.AUTH_USER or not cls.AUTH_PASS or not cls.BASE_URL:
            raise ValueError("WordPress の認証情報が不足しています。AUTH_USER, AUTH_PASS, BASE_URL を設定してください。")
        
        if not cls.GEMINI_API_KEY:
            raise ValueError("Gemini API キーが設定されていません。GEMINI_API_KEY を設定してください。")
        
        # Qiita トークンは必須ではないが、設定されていない場合は警告を出す
        if not cls.QIITA_TOKEN:
            print("警告: Qiita API トークンが設定されていません。Qiita への投稿機能は無効です。")

    @classmethod
    def setup(cls):
        """環境変数を設定し、設定の妥当性を検証するメソッド"""
        # Gemini API キーを環境変数に設定
        os.environ["GEMINI_API_KEY"] = cls.GEMINI_API_KEY or "YOUR_DEFAULT_API_KEY_HERE"
        
        # 設定の妥当性を検証
        cls.validate()

# 設定のセットアップを実行
Config.setup()
