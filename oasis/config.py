import os
from dotenv import load_dotenv
from .logger import logger  # logger をインポート

# 現在の作業ディレクトリの.envファイルを読み込む
load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))

class Config:
    # WordPress設定
    AUTH_USER = os.getenv('AUTH_USER')
    AUTH_PASS = os.getenv('AUTH_PASS')
    BASE_URL = os.getenv('BASE_URL')
    
    # LLM設定
    LLM_MODEL = os.getenv('LLM_MODEL', 'gemini/gemini-1.5-pro-latest')  # デフォルトモデル
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '10'))  # LLMリクエストの最大リトライ回数
    
    # Qiita設定
    QIITA_TOKEN = os.getenv('QIITA_TOKEN')
    QIITA_POST_PUBLISH = os.getenv('QIITA_POST_PUBLISH', 'false').lower() == 'true'
    
    # Note設定
    NOTE_EMAIL = os.getenv('NOTE_EMAIL')
    NOTE_PASSWORD = os.getenv('NOTE_PASSWORD')
    NOTE_USER_ID = os.getenv('NOTE_USER_ID')
    NOTE_PUBLISH = os.getenv('NOTE_PUBLISH', 'false').lower() == 'true'
    NOTE_API_VER = os.getenv('NOTE_API_VER', 'v2')
    
    # Zenn設定
    ZENN_OUTPUT_PATH = os.getenv('ZENN_OUTPUT_PATH', r"C:\Prj\Zenn\articles")
    ZENN_PUBLISH = os.getenv('ZENN_PUBLISH', 'false').lower() == 'true'
    
    # Firefox設定
    FIREFOX_BINARY_PATH = os.getenv('FIREFOX_BINARY_PATH')
    FIREFOX_PROFILE_PATH = os.getenv('FIREFOX_PROFILE_PATH')
    FIREFOX_HEADLESS = os.getenv('FIREFOX_HEADLESS', 'false').lower() == 'true'
    
    # WebUI用の下書きフォルダのパス
    WEBUI_DRAFT_DIR = os.getenv('WEBUI_DRAFT_DIR', os.path.join(os.getcwd(), "draft"))

    # WordPressのエンドポイント
    END_POINT_URL = f"{BASE_URL}/wp-json/wp/v2/posts/" if BASE_URL else None
    MEDIA_ENDPOINT = f"{BASE_URL}/wp-json/wp/v2/media" if BASE_URL else None

    # Gemini API キー
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

    @classmethod
    def validate(cls):
        """設定の妥当性を検証するメソッド"""
        if not cls.AUTH_USER or not cls.AUTH_PASS or not cls.BASE_URL:
            logger.warning(
                "WordPress の認証情報が不足しています。AUTH_USER, AUTH_PASS, BASE_URL を設定してください。"
            )
        else:
            logger.info(f"WordPress AUTH_USER: {cls.AUTH_USER[:3]}")
            logger.info(f"WordPress BASE_URL: {cls.BASE_URL[:3]}")  # パスワードは表示しない

        if not cls.GEMINI_API_KEY:
            logger.warning(
                "Gemini API キーが設定されていません。GEMINI_API_KEY を設定してください。"
            )
        else:
            logger.info(f"Gemini API Key: {cls.GEMINI_API_KEY[:3]}") 

        # Qiita トークンは必須ではないが、設定されていない場合は警告を出す
        if not cls.QIITA_TOKEN:
            logger.warning(
                "Qiita API トークンが設定されていません。Qiita への投稿機能は無効です。"
            )
        else:
            logger.info(f"Qiita Token: {cls.QIITA_TOKEN[:3]}") 
        
        # Note ログイン情報は必須ではないが、設定されていない場合は警告を出す
        if not cls.NOTE_EMAIL or not cls.NOTE_PASSWORD or not cls.NOTE_USER_ID:
            logger.warning(
                "Note ログイン情報が設定されていません。Note への投稿機能は無効です。"
            )
        else:
            logger.info(f"Note Email: {cls.NOTE_EMAIL[:3]}")
            logger.info(f"Note User ID: {cls.NOTE_USER_ID[:3]}") # パスワードは表示しない

    @classmethod
    def setup(cls):
        """環境変数を設定し、設定の妥当性を検証するメソッド"""
        # Gemini API キーを環境変数に設定
        os.environ["GEMINI_API_KEY"] = (
            cls.GEMINI_API_KEY or "YOUR_DEFAULT_API_KEY_HERE"
        )

        # 設定の妥当性を検証
        cls.validate()


# 設定のセットアップを実行
Config.setup()
