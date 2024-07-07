import os
import re
import time
from random import randint
from typing import Optional, List, Dict

from bs4 import BeautifulSoup
from markdown import markdown
from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

import markdown
from markdown.extensions import codehilite, fenced_code
from bs4 import BeautifulSoup
from selenium import webdriver
from logging import getLogger

import mistune

from janome.tokenizer import Tokenizer

from .markdown_processor import MarkdownProcessor

from art import *

class NoteAPIV2:
    def __init__(
        self,
        email: str,
        password: str,
        user_id: str,
        firefox_binary_path: Optional[str] = None,
        firefox_profile_path: Optional[str] = None,
    ):
        """NoteArticlePublisherを初期化します。

        Args:
            email (str): Noteアカウントのメールアドレス
            password (str): Noteアカウントのパスワード
            user_id (str): NoteのユーザーID
            firefox_binary_path (Optional[str], optional): Firefoxのバイナリパス. Defaults to None.
            firefox_profile_path (Optional[str], optional): Firefoxのプロファイルパス. Defaults to None.
        """
        
        self.email = email
        self.password = password
        self.user_id = user_id
        self.firefox_binary_path = firefox_binary_path
        self.firefox_profile_path = firefox_profile_path

    def __str__(self) -> str:
        return f"Email : {self.email} / User ID : {self.user_id}"

    def _init_driver(self, headless: bool = False) -> webdriver.Firefox:
        """WebDriverを初期化します。

        Args:
            headless (bool, optional): ヘッドレスモードで起動するかどうか. Defaults to False.

        Returns:
            webdriver.Firefox: 初期化されたWebDriverインスタンス
        """
        logger.info("WebDriverを初期化しています...")

        options = Options()
        if headless:
            options.add_argument("--headless")

        # ユーザーエージェントを設定
        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )
        options.set_preference("general.useragent.override", user_agent)

        # Firefox のパスを設定
        if self.firefox_binary_path:
            options.binary_location = self.firefox_binary_path
        elif os.getenv("FIREFOX_BINARY_PATH"):
            options.binary_location = os.getenv("FIREFOX_BINARY_PATH")

        # Firefox のプロファイルパスを設定
        if self.firefox_profile_path:
            options.add_argument(f"-profile {self.firefox_profile_path}")
        elif os.getenv("FIREFOX_PROFILE_PATH"):
            options.add_argument(f'-profile {os.getenv("FIREFOX_PROFILE_PATH")}')

        logger.debug(f"profile_path : {self.firefox_profile_path}")
        logger.debug(f"firefox_binary : {self.firefox_binary_path}")

        # GeckoDriverManagerを使用してドライバーを管理
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)

        # ウィンドウサイズを設定
        driver.set_window_size(1920, 1080)

        logger.success("WebDriverの初期化が完了しました。")
        return driver

    def _login(self, driver: webdriver.Firefox) -> None:
        """Noteにログインします。

        Args:
            driver (webdriver.Firefox): WebDriverインスタンス
        """
        try:
            logger.info("Noteにログインしています...")
            driver.get("https://note.com/login?redirectPath=%2Fnotes%2Fnew")

            wait = WebDriverWait(driver, 10)

            time.sleep(5)
            email_input = wait.until(EC.presence_of_element_located((By.ID, "email")))
            email_input.send_keys(self.email)
            time.sleep(0.5)
            password_input = wait.until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            password_input.send_keys(self.password)
            time.sleep(0.5)
            login_button = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, ".o-login__button button")
                )
            )
            login_button.click()
            time.sleep(2)

        except Exception:
            logger.info("Noteに自動ログインしました...")
            driver.get("https://editor.note.com/new")
            WebDriverWait(driver, 10)
            time.sleep(2)

        logger.success("Noteへのログインが完了しました。")

    def _input_title(self, driver: webdriver.Firefox, title: str) -> None:
        """記事のタイトルを入力します。

        Args:
            driver (webdriver.Firefox): WebDriverインスタンス
            title (str): 記事のタイトル
        """
        logger.info("記事のタイトルを入力しています...")
        textarea = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "textarea"))
        )
        textarea.click()
        textarea.send_keys(title)
        textarea.send_keys(Keys.ENTER)
        logger.success("記事のタイトル入力が完了しました。")

    def _load_markdown_content(
        self, file_name: Optional[str] = None, text: Optional[str] = None
    ) -> str:
        """記事コンテンツをファイルまたはテキストから読み込みます。

        Args:
            file_name (Optional[str], optional): 記事コンテンツファイル名. Defaults to None.
            text (Optional[str], optional): 記事コンテンツテキスト. Defaults to None.

        Returns:
            str: 記事コンテンツ
        """
        logger.info("記事コンテンツを読み込んでいます...")
        if text is None:
            with open(file=file_name, mode="r", encoding="utf-8") as f:
                text = f.read()
        logger.success("記事コンテンツの読み込みが完了しました。")
        return text


    def _input_content(self, driver: webdriver.Firefox, content: str) -> None:
        """記事の内容を入力し、HTMLとして保存します。"""
        logger.info("記事の内容を入力しています...")
        
        # マークダウンをHTMLに変換（コードブロックを適切に処理）
        # html_content = convert_markdown_to_html(content)

        processor = MarkdownProcessor()
        html_content = processor.convert_markdown_to_html(content)

        # BeautifulSoupを使ってHTMLをパースする（必要に応じて）
        soup = BeautifulSoup(html_content, "html.parser")

        # HTMLを一括挿入するためのJavaScriptコード
        script = """
            var el = arguments[0];
            var html = arguments[1];
            el.innerHTML += html;

            var range = document.createRange();
            range.selectNodeContents(el);
            range.collapse(false);
            var selection = window.getSelection();
            selection.removeAllRanges();
            selection.addRange(range);

            el.scrollTop = el.scrollHeight;
        """

        # 記事入力エリアの要素を取得
        active_element = driver.switch_to.active_element

        # JavaScriptを実行してHTMLを一括挿入
        driver.execute_script(script, active_element, str(soup))

        logger.success("記事の内容入力が完了しました。")

        # HTMLをローカルに保存
        save_html_locally(str(soup), "saved_article.html")

    def _scroll_page(self, driver: webdriver.Firefox) -> None:
        """ページをスクロールします。

        Args:
            driver (webdriver.Firefox): WebDriverインスタンス
        """
        logger.info("ページをスクロールしています...")
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(1)
        logger.success("ページのスクロールが完了しました。")

    def _set_thumbnail(
        self,
        driver: webdriver.Firefox,
        wait: WebDriverWait,
        search_word: str,
        image_index: int or str,
    ) -> None:
        """サムネイル画像を設定します。"""
        logger.info("サムネイル画像を設定しています...")
        time.sleep(2)
        button = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/main/div[1]/button",
                )
            )
        )
        logger.debug(f"button: {button}")  # ボタンのテキストをデバッグ出力
        button.click()

        time.sleep(2)
        button = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/main/div[1]/div/div[2]/button",
                )
            )
        )
        logger.debug(f"button: {button}")  # ボタンのテキストをデバッグ出力
        button.click()

        time.sleep(2)
        button = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[5]/div/div/div[1]/div/div[2]/button")
            )
        )
        button.click()
        time.sleep(2)
        keyword_input = driver.switch_to.active_element
        keyword_input.send_keys("illust sample")
        time.sleep(3)
        button = driver.find_element(
            By.XPATH, "/html/body/div[5]/div/div/div[1]/div/div[2]/button"
        )
        button.click()
        time.sleep(3)
        parent_element = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[5]/div/div/div[2]")
            )
        )
        img_elements = parent_element.find_elements(By.TAG_NAME, "img")

        index = self._select_image_index(image_index, img_elements)

        if index < 0 or isinstance(image_index, type(None)):
            keyword_input.send_keys(Keys.ESCAPE)
        else:
            img_elements[index].click()
            button = wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[5]/div/div/div[2]/div/div[2]/div/div[5]/button[2]",
                    )
                )
            )
            button.click()
            time.sleep(5)
            button = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[4]/div/div/div[3]/button[2]")
                )
            )
            button.click()
            time.sleep(20)
        logger.success("サムネイル画像の設定が完了しました。")

    def _select_image_index(
        self, image_index: int or str, img_elements: list
    ) -> int:
        """画像のインデックスを選択します。

        Args:
            image_index (int or str): 画像インデックス (random, None, またはインデックス番号)
            img_elements (list): 画像要素のリスト

        Returns:
            int: 選択された画像インデックス
        """
        if isinstance(image_index, int) and 0 <= int(
            image_index
        ) <= int(len(img_elements) - 1):
            return image_index
        elif image_index == "random":
            max_index = len(img_elements) - 1
            return randint(0, max_index) if max_index >= 0 else -1
        else:
            return -1

    def _set_tags(
        self, driver: webdriver.Firefox, wait: WebDriverWait, input_tag_list: list
    ) -> None:
        """タグを設定します。"""
        logger.info("タグを設定しています...")
        time.sleep(1)
        input_element = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[1]/div[3]/div[1]/div[2]/main/section[1]/div[2]/div/div[1]/input",
                )
            )
        )
        input_element.click()
        time.sleep(0.5)
        input = driver.switch_to.active_element
        for tag in input_tag_list:
            time.sleep(0.5)
            logger.debug(f"tag : [{tag}]")
            input.send_keys(tag.replace(" ", "").replace(".", ""))
            time.sleep(0.5)
            input = driver.switch_to.active_element
            input.send_keys(Keys.SPACE)
        logger.success("タグの設定が完了しました。")

    def _publish_article(
        self, driver: webdriver.Firefox, wait: WebDriverWait, input_tag_list: list
    ) -> Dict:
        """記事を公開します。"""
        logger.info("記事を公開しています...")
        button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/header/div/div[2]/div/button[2]",
                )
            )
        )
        button.click()
        time.sleep(2)

        # タグ設定処理を呼び出す
        self._set_tags(driver, wait, input_tag_list)

        button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/div/button")
            )
        )
        button.click()

        url = driver.current_url
        cut_url = url.split("/")
        post_id = cut_url[4]
        post_url = f"https://note.com/{self.user_id}/n/{post_id}"

        logger.success(f"記事が公開されました。URL: {post_url}")
        return {
            "run": "success",
            "post_setting": "Public",
            "post_url": post_url,
        }

    def _save_draft(self, driver: webdriver.Firefox, wait: WebDriverWait) -> Dict:
        """記事を下書き保存します。"""
        logger.info("記事を下書き保存しています...")
        button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/header/div/div[2]/div/button[1]",
                )
            )
        )
        button.click()
        logger.success("記事が下書き保存されました。")
        return {"run": "success", "post_setting": "Draft"}

    def create_article(
        self,
        title: str,
        input_tag_list: List[str],
        image_index: Optional[str] = "random",
        post_setting: bool = False,
        file_name: Optional[str] = None,
        headless: bool = True,
        text: Optional[str] = None,
    ) -> Dict:
        """新規記事を作成します。

        Args:
            title (str): 記事のタイトル
            input_tag_list (List[str]): 記事のタグリスト
            image_index (Optional[str], optional): 記事画像のインデックス番号 (random, None, またはインデックス番号). Defaults to 'random'.
            post_setting (bool, optional): 下書き保存するか公開するか (デフォルトは下書き保存). Defaults to False.
            file_name (Optional[str], optional): 記事コンテンツファイル名. Defaults to None.
            headless (bool, optional): ヘッドレスモードで起動するかどうか. Defaults to True.
            text (Optional[str], optional): 記事コンテンツテキスト. Defaults to None.

        Returns:
            Dict: 実行結果
        """
        tprint('>>  NoteAPIV2')
        logger.info("記事の作成を開始します...")
        if not all(
            [
                title,
                input_tag_list,
                isinstance(input_tag_list, list),
                (
                    image_index == "random"
                    or isinstance(image_index, (int, type(None)))
                ),
                (file_name is not None or text is not None),
            ]
        ):
            logger.error("必須データがありません。")
            return {"run": "error", "message": "必須データがありません。"}

        driver = self._init_driver(headless)
        self._login(driver)
        self._input_title(driver, title)

        content = self._load_markdown_content(file_name, text)
        self._input_content(driver, content)

        self._scroll_page(driver)

        search_word = "sample"
        wait = WebDriverWait(driver, 10)
        self._set_thumbnail(driver, wait, search_word, image_index)

        if post_setting:
            res = self._publish_article(driver, wait, input_tag_list)
        else:
            res = self._save_draft(driver, wait)

        res.update(
            {"title": title, "file_path": file_name, "tag_list": input_tag_list}
        )
        driver.quit()
        logger.success(" 記事の作成が完了しました。")
        return res

def save_html_locally(html_content: str, filename: str) -> None:
    """HTMLコンテンツをローカルファイルに保存します。"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        logger.success(f"HTMLを'{filename}'に保存しました。")
    except IOError as e:
        logger.error(f"ファイルの保存中にエラーが発生しました: {e}")
