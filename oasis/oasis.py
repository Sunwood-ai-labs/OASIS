from .services.file_handler import FileHandler
from .services.wordpress_api import WordPressAPI
from .services.llm_api import LLMService
from .services.qiita_api import QiitaAPI
from .services.note_api_v1 import NoteAPI
from .services.note_api_v2 import NoteAPIV2
from .models.post import Post
from .logger import logger
from .config import Config
from .exceptions import APIError
from tqdm import tqdm
import os
import json

class OASIS:
    def __init__(
        self,
        base_url=None,
        auth_user=None,
        auth_pass=None,
        llm_model=None,
        max_retries=3,
        qiita_token=None,
        qiita_post_private=None,
        note_email=None,
        note_password=None,
        note_user_id=None,
        note_publish=None,
        firefox_binary_path=None,  # Firefox のパスを追加
        firefox_profile_path=None,  # Firefox のプロファイルパスを追加
        firefox_headless=False,
        note_api_ver = "v2",
    ):
        self.config = Config()
        if base_url:
            self.config.BASE_URL = base_url
        if auth_user:
            self.config.AUTH_USER = auth_user
        if auth_pass:
            self.config.AUTH_PASS = auth_pass
        if llm_model:
            self.config.LLM_MODEL = llm_model
        if qiita_token:
            self.config.QIITA_TOKEN = qiita_token
        if note_email:
            self.config.NOTE_EMAIL = note_email
        if note_password:
            self.config.NOTE_PASSWORD = note_password
        if note_user_id:
            self.config.NOTE_USER_ID = note_user_id

        # WordPress API の初期化は、必要な場合にのみ行う
        try:
            self.wp_api = WordPressAPI(
                self.config.BASE_URL, self.config.AUTH_USER, self.config.AUTH_PASS
            )
        except Exception as e:
            logger.warning(f"WordPress API の初期化に失敗しました: {str(e)}")


        self.llm_service = LLMService(max_retries=max_retries)

        if self.config.QIITA_TOKEN:
            self.qiita_api = QiitaAPI(token=self.config.QIITA_TOKEN, 
                                        post_private=qiita_post_private)

        # Note API の初期化は、必要な情報が設定されている場合にのみ行う
        if self.config.NOTE_EMAIL and self.config.NOTE_PASSWORD and self.config.NOTE_USER_ID:

            if(note_api_ver == "v2"):
                self.note_api = NoteAPIV2(
                    self.config.NOTE_EMAIL, 
                    self.config.NOTE_PASSWORD, 
                    self.config.NOTE_USER_ID,
                    firefox_binary_path=firefox_binary_path,
                    firefox_profile_path=firefox_profile_path
                )
            else:
                self.note_api = NoteAPI(
                    self.config.NOTE_EMAIL, 
                    self.config.NOTE_PASSWORD, 
                    self.config.NOTE_USER_ID,
                    firefox_binary_path=firefox_binary_path,
                    firefox_profile_path=firefox_profile_path
                )
        self.note_publish = note_publish
        self.firefox_headless = firefox_headless


    def process_folder(
        self, folder_path: str, post_to_qiita: bool = False, post_to_note: bool = False, post_to_wp: bool = False, slug = "test_slug", 
    ):

        file_handler = FileHandler(folder_path)

        logger.info("Markdownファイルの読み込みを開始します...")
        markdown_content, title = file_handler.read_markdown()
        logger.info(f"Markdownファイルの読み込みが完了しました: タイトル '{title}'")

        logger.info("サムネイル画像の検索を開始します...")
        thumbnail_path = file_handler.get_thumbnail()
        if thumbnail_path:
            logger.info(f"サムネイル画像が見つかりました: {thumbnail_path}")
        else:
            logger.info("サムネイル画像が見つかりませんでした。")

        # Create a folder to store JSON files
        json_folder = os.path.join("data", "wp_data")
        os.makedirs(json_folder, exist_ok=True)

        category_map_path = os.path.join(json_folder, "category_map.json")
        tag_map_path = os.path.join(json_folder, "tag_map.json")

        if post_to_wp:
            logger.info("既存のカテゴリとタグの取得を開始します...")
            category_map, tag_map = self.wp_api.get_existing_categories_and_tags()

            # Save category_map and tag_map to JSON files
            with open(category_map_path, 'w', encoding="utf-8") as f:
                json.dump(category_map, f, ensure_ascii=False, indent=4)
            with open(tag_map_path, 'w', encoding="utf-8") as f:
                json.dump(tag_map, f, ensure_ascii=False, indent=4)

            logger.info("英語のスラグ生成を開始します...")
            slug = self.llm_service.generate_english_slug(title)
            logger.info(f"英語のスラグ生成が完了しました: {slug}")
        else:
            # Load category_map and tag_map from JSON files if they exist
            if os.path.exists(category_map_path):
                with open(category_map_path, 'r', encoding="utf-8") as f:
                    category_map = json.load(f)
            else:
                category_map = {}

            if os.path.exists(tag_map_path):
                with open(tag_map_path, 'r', encoding="utf-8") as f:
                    tag_map = json.load(f)
            else:
                tag_map = {}

        logger.info("カテゴリとタグの提案を開始します...")
        suggestions = self.llm_service.suggest_categories_and_tags(
            markdown_content, category_map.keys(), tag_map.keys()
        )
        logger.info(
            f"カテゴリとタグの提案が完了しました: カテゴリ {len(suggestions['categories'])}, タグ {len(suggestions['tags'])}"
        )

        post = Post(
            title, markdown_content, slug, suggestions['categories'], suggestions['tags']
        )

        if post_to_wp:
            logger.info("WordPressへの投稿を開始します...")
            post_id = self.wp_api.create_post(post)
            logger.info(f"WordPressへの投稿が完了しました: ID {post_id}")

            if thumbnail_path:
                logger.info("サムネイル画像のアップロードを開始します...")
                self.wp_api.upload_thumbnail(post_id, thumbnail_path)
                logger.info("サムネイル画像のアップロードが完了しました。")

        if post_to_qiita and self.config.QIITA_TOKEN:
            logger.info("Qiitaへの投稿を開始します...")
            qiita_post_id = self.qiita_api.create_post(post)
            logger.info(f"Qiitaへの投稿が完了しました: ID {qiita_post_id}")

        if post_to_note and hasattr(self, 'note_api'):
            logger.info("Noteへの投稿を開始します...")
            tags = [tag["name"] for tag in post.tags]
            note_result = self.note_api.create_article(title, tags, text=markdown_content, headless=self.firefox_headless, post_setting=self.note_publish)
            logger.info(f"Noteへの投稿が完了しました: {note_result}")

        logger.info("投稿処理が正常に完了しました。")
        return post.to_dict()


    def set_llm_model(self, model: str):
        self.config.LLM_MODEL = model
        self.llm_service = LLMService()
        logger.info(f"LLMモデルを変更しました: {model}")
