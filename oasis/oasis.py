
try:
    from .services.file_handler import FileHandler

    from .services.wordpress_api import WordPressAPI
    from .services.wordpress_api import convert_markdown_to_html_with_mermaid, convert_html_to_markdown_preserve_mermaid

    from .services.llm_api import LLMService
    from .services.qiita_api import QiitaAPI

    from .services.note_api_v1 import NoteAPI
    from .services.note_api_v2 import NoteAPIV2, process_markdown_mermaid_blocks

    from .services.ZennAPI_v1 import ZennAPI
    from .services.ZennAPI_v2 import ZennAPIV2

    from .models.post import Post
    from .logger import logger
    from .config import Config
    from .exceptions import APIError
except:
    from oasis.services.file_handler import FileHandler

    from oasis.services.wordpress_api import WordPressAPI
    from oasis.services.wordpress_api import convert_markdown_to_html_with_mermaid, convert_html_to_markdown_preserve_mermaid

    from oasis.services.llm_api import LLMService
    from oasis.services.qiita_api import QiitaAPI

    from oasis.services.note_api_v1 import NoteAPI
    from oasis.services.note_api_v2 import NoteAPIV2, process_markdown_mermaid_blocks

    from oasis.services.ZennAPI_v1 import ZennAPI
    from oasis.services.ZennAPI_v2 import ZennAPIV2

    from oasis.models.post import Post
    from oasis.logger import logger
    from oasis.config import Config
    from oasis.exceptions import APIError

import streamlit as st
from functools import wraps
from tqdm import tqdm
import os
import json


def spinner_and_success(message):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with st.spinner(message):
                result = func(*args, **kwargs)
            st.success(f"{message}完了しました！")
            return result
        return wrapper
    return decorator

class OASIS:
    def __init__(
        self,
        base_url=None,
        auth_user=None,
        auth_pass=None,
        llm_model=None,
        max_retries=3,
        qiita_token=None,
        qiita_post_private=True,
        note_email=None,
        note_password=None,
        note_user_id=None,
        note_publish=None,
        firefox_binary_path=None,  # Firefox のパスを追加
        firefox_profile_path=None,  # Firefox のプロファイルパスを追加
        firefox_headless=False,
        note_api_ver = "v2",
        zenn_api_ver = "v2",
        zenn_output_path = None
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
        
        
        # ZennAPIのインスタンスを作成
        self.zenn_api = ZennAPI(
            firefox_binary_path=firefox_binary_path,
            firefox_profile_path=firefox_profile_path
        )
        self.zenn_api_v2 = ZennAPIV2()
        self.zenn_output_path = zenn_output_path
        
        self.firefox_headless = firefox_headless


    def process_folder(
        self, folder_path: str, 
        post_to_qiita: bool = False, 
        post_to_note: bool = False, 
        post_to_wp: bool = False, 
        post_to_zenn: bool = False, 
        slug = "test_slug", 
    ):
        # FileHandlerのインスタンスを作成
        file_handler = FileHandler(folder_path)

        # Markdownファイルを読み込み、内容とタイトルを取得
        markdown_content, title = self.read_markdown(file_handler)
        
        # Note用にMarkdownを前処理
        note_mermaid_md = self.preprocess_for_note(markdown_content)
        
        # サムネイル画像を検索
        thumbnail_path = self.find_thumbnail(file_handler)
        
        # カテゴリとタグの情報を読み込みまたは取得
        category_map, tag_map = self.load_or_fetch_categories_and_tags(post_to_wp)
        
        # 記事のスラグ（URL用の識別子）を生成
        slug = self.generate_slug(title)
        
        # 記事のカテゴリとタグを提案
        suggestions = self.suggest_categories_and_tags(markdown_content, category_map, tag_map)
        
        # 投稿用のPostオブジェクトを作成
        post = self.create_post(title, markdown_content, slug, suggestions)
        
        # WordPressに投稿
        if post_to_wp:
            self.post_to_wordpress(post, thumbnail_path)
        
        # Qiitaに投稿
        if post_to_qiita:
            self.post_to_qiita(post)
        
        # Noteに投稿
        if post_to_note:
            self.post_to_note(post, note_mermaid_md)
        
        # Zennに投稿
        if post_to_zenn:
            self.post_to_zenn(post, thumbnail_path)

        logger.info("投稿処理が正常に完了しました。")
        return post.to_dict()


    @spinner_and_success('Markdownファイルを読み込んでいます...')
    def read_markdown(self, file_handler):
        markdown_content, title = file_handler.read_markdown()
        logger.info(f"Markdownファイルの読み込みが完了しました: タイトル '{title}'")
        return markdown_content, title

    @spinner_and_success('Noteのための前処理を行っています...')
    def preprocess_for_note(self, markdown_content):
        return process_markdown_mermaid_blocks(markdown_content)

    @spinner_and_success('サムネイル画像を検索しています...')
    def find_thumbnail(self, file_handler):
        thumbnail_path = file_handler.get_thumbnail()
        if thumbnail_path:
            logger.info(f"サムネイル画像が見つかりました: {thumbnail_path}")
        else:
            logger.info("サムネイル画像が見つかりませんでした。")
        return thumbnail_path

    @spinner_and_success('カテゴリとタグを読み込み/取得しています...')
    def load_or_fetch_categories_and_tags(self, post_to_wp):
        json_folder = os.path.join("data", "wp_data")
        os.makedirs(json_folder, exist_ok=True)
        category_map_path = os.path.join(json_folder, "category_map.json")
        tag_map_path = os.path.join(json_folder, "tag_map.json")

        if post_to_wp:
            category_map, tag_map = self.wp_api.get_existing_categories_and_tags()
            with open(category_map_path, 'w', encoding="utf-8") as f:
                json.dump(category_map, f, ensure_ascii=False, indent=4)
            with open(tag_map_path, 'w', encoding="utf-8") as f:
                json.dump(tag_map, f, ensure_ascii=False, indent=4)
        else:
            category_map = json.load(open(category_map_path, 'r', encoding="utf-8")) if os.path.exists(category_map_path) else {}
            tag_map = json.load(open(tag_map_path, 'r', encoding="utf-8")) if os.path.exists(tag_map_path) else {}

        return category_map, tag_map

    @spinner_and_success('英語のスラグを生成しています...')
    def generate_slug(self, title):
        slug = self.llm_service.generate_english_slug(title)
        logger.info(f"英語のスラグ生成が完了しました: {slug}")
        return slug

    @spinner_and_success('カテゴリとタグを提案しています...')
    def suggest_categories_and_tags(self, markdown_content, category_map, tag_map):
        suggestions = self.llm_service.suggest_categories_and_tags(
            markdown_content, category_map.keys(), tag_map.keys()
        )
        logger.info(
            f"カテゴリとタグの提案が完了しました: カテゴリ {len(suggestions['categories'])}, タグ {len(suggestions['tags'])}"
        )
        return suggestions

    def create_post(self, title, markdown_content, slug, suggestions):
        return Post(
            title, markdown_content, slug, suggestions['categories'], suggestions['tags']
        )

    @spinner_and_success('WordPressに投稿しています...')
    def post_to_wordpress(self, post, thumbnail_path):
        post_id = self.wp_api.create_post(post)
        logger.info(f"WordPressへの投稿が完了しました: ID {post_id}")

        if thumbnail_path:
            logger.info("サムネイル画像のアップロードを開始します...")
            self.wp_api.upload_thumbnail(post_id, thumbnail_path)
            logger.info("サムネイル画像のアップロードが完了しました。")

    @spinner_and_success('Qiitaに投稿しています...')
    def post_to_qiita(self, post):
        if self.config.QIITA_TOKEN:
            qiita_post_id = self.qiita_api.create_post(post)
            logger.info(f"Qiitaへの投稿が完了しました: ID {qiita_post_id}")

    @spinner_and_success('Noteに投稿しています...')
    def post_to_note(self, post, note_mermaid_md):
        if hasattr(self, 'note_api'):
            tags = [tag["name"] for tag in post.tags]
            note_result = self.note_api.create_article(post.title, tags, text=note_mermaid_md, headless=self.firefox_headless, post_setting=self.note_publish)
            logger.info(f"Noteへの投稿が完了しました: {note_result}")

    @spinner_and_success('Zennに投稿しています...')
    def post_to_zenn(self, post, thumbnail_path):
        tags = [tag["name"] for tag in post.tags]
        self.zenn_api_v2.create_article(
            title=post.title,
            slug=post.slug,
            content_md=post.content,
            type="tech",
            topics=tags[:4],
            image_file=thumbnail_path,
            output_dir=self.zenn_output_path
        )

    def set_llm_model(self, model: str):
        self.config.LLM_MODEL = model
        self.llm_service = LLMService()
        logger.info(f"LLMモデルを変更しました: {model}")
