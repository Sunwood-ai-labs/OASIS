from .services.file_handler import FileHandler
from .services.wordpress_api import WordPressAPI
from .services.llm_api import LLMService
from .services.qiita_api import QiitaAPI
from .services.note_api import NoteAPI
from .models.post import Post
from .logger import logger
from .config import Config
from .exceptions import APIError

class OASIS:
    def __init__(
        self,
        base_url=None,
        auth_user=None,
        auth_pass=None,
        llm_model=None,
        max_retries=3,
        qiita_token=None,
        note_email=None,
        note_password=None,
        note_user_id=None,
        note_publish=None
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
        if note_publish:
            self.note_publish = note_publish
        try:
            self.wp_api = WordPressAPI(
                self.config.BASE_URL, self.config.AUTH_USER, self.config.AUTH_PASS
            )
        except APIError as e:
            logger.error(f"WordPress API の初期化に失敗しました: {str(e)}")
            raise

        self.llm_service = LLMService(max_retries=max_retries)

        if self.config.QIITA_TOKEN:
            self.qiita_api = QiitaAPI(self.config.QIITA_TOKEN)

        if self.config.NOTE_EMAIL and self.config.NOTE_PASSWORD and self.config.NOTE_USER_ID:
            self.note_api = NoteAPI(
                self.config.NOTE_EMAIL, self.config.NOTE_PASSWORD, self.config.NOTE_USER_ID
            )

    def process_folder(
        self, folder_path: str, post_to_qiita: bool = False, post_to_note: bool = False
    ):
        try:
            file_handler = FileHandler(folder_path)

            logger.info("Markdownファイルの読み込みを開始")
            markdown_content, title = file_handler.read_markdown()
            logger.info(f"Markdownファイルの読み込みが完了: タイトル '{title}'")

            logger.info("サムネイル画像の検索を開始")
            thumbnail_path = file_handler.get_thumbnail()
            if thumbnail_path:
                logger.info(f"サムネイル画像が見つかりました: {thumbnail_path}")
            else:
                logger.info("サムネイル画像が見つかりませんでした")

            logger.info("既存のカテゴリとタグの取得を開始")
            category_map, tag_map = self.wp_api.get_existing_categories_and_tags()

            logger.info("カテゴリとタグの提案を開始")
            suggestions = self.llm_service.suggest_categories_and_tags(
                markdown_content, category_map.keys(), tag_map.keys()
            )
            logger.info(
                f"カテゴリとタグの提案が完了: カテゴリ {len(suggestions['categories'])}, タグ {len(suggestions['tags'])}"
            )

            logger.info("英語のスラグ生成を開始")
            slug = self.llm_service.generate_english_slug(title)
            logger.info(f"英語のスラグ生成が完了: {slug}")

            post = Post(
                title, markdown_content, slug, suggestions['categories'], suggestions['tags']
            )

            # logger.info("WordPressへの投稿を開始")
            # post_id = self.wp_api.create_post(post)
            # logger.info(f"WordPressへの投稿が完了: ID {post_id}")

            # if thumbnail_path:
            #     logger.info("サムネイル画像のアップロードを開始")
            #     self.wp_api.upload_thumbnail(post_id, thumbnail_path)
            #     logger.info("サムネイル画像のアップロードが完了")

            # if post_to_qiita and self.config.QIITA_TOKEN:
            #     logger.info("Qiitaへの投稿を開始")
            #     qiita_post_id = self.qiita_api.create_post(post)
            #     logger.info(f"Qiitaへの投稿が完了: ID {qiita_post_id}")

            if post_to_note and self.config.NOTE_EMAIL and self.config.NOTE_PASSWORD and self.config.NOTE_USER_ID:
                logger.info("Noteへの投稿を開始")
                tags = [tag["name"] for tag in post.tags]  # タグ名をリストに変換
                note_result = self.note_api.create_article(title, tags, text=markdown_content, post_setting=self.note_publish)
                logger.info(f"Noteへの投稿が完了: {note_result}")

            logger.info("投稿処理が正常に完了しました")
            return post.to_dict()

        except APIError as e:
            logger.error(f"API エラーが発生しました: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"予期せぬエラーが発生しました: {str(e)}")
            raise

    def set_llm_model(self, model: str):
        self.config.LLM_MODEL = model
        self.llm_service = LLMService()
        logger.info(f"LLMモデルを変更しました: {model}")
