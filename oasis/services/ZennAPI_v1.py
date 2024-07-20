import time
import os
from typing import Optional, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.action_chains import ActionChains

from loguru import logger
from art import *

class ZennAPI:
    def __init__(
        self,
        firefox_binary_path: Optional[str] = None,
        firefox_profile_path: Optional[str] = None,
    ):
        # Firefoxのバイナリとプロファイルのパスを設定
        self.firefox_binary_path = firefox_binary_path
        self.firefox_profile_path = firefox_profile_path
        self.driver = None

    def initialize_driver(self, headless: bool = False):
        # WebDriverの初期化
        logger.info("WebDriverを初期化しています...")
        options = Options()
        if headless:
            options.add_argument("--headless")

        # Firefox のパスを設定
        if self.firefox_binary_path:
            options.binary_location = self.firefox_binary_path
        elif os.getenv("FIREFOX_BINARY_PATH"):
            options.binary_location = os.getenv("FIREFOX_BINARY_PATH")

        # Firefox のプロファイルパスを設定
        if self.firefox_profile_path:
            options.add_argument(f"-profile {self.firefox_profile_path}")
            options.profile = webdriver.FirefoxProfile(self.firefox_profile_path)
        elif os.getenv("FIREFOX_PROFILE_PATH"):
            options.profile = webdriver.FirefoxProfile(os.getenv("FIREFOX_PROFILE_PATH"))

        service = Service(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=service, options=options)
        self.driver.set_window_size(1920, 1080)
        logger.success("WebDriverの初期化が完了しました。")

    def navigate_to_url(self, url: str):
        # 指定されたURLに移動
        logger.info(f"{url} に移動しています...")
        self.driver.get(url)
        time.sleep(2)
        logger.success(f"{url} への移動が完了しました。")

    def click_button(self, selector: str, wait_time: int = 10):
        # 指定されたセレクタの要素をクリック
        logger.info(f"{selector} ボタンをクリックしています...")
        wait = WebDriverWait(self.driver, wait_time)
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        button.click()
        time.sleep(1)
        logger.success(f"{selector} ボタンのクリックが完了しました。")

    def fill_text_input(self, selector: str, text: str, wait_time: int = 10):
        # 指定されたセレクタの入力フィールドにテキストを入力
        logger.info(f"{selector} に '{text}' を入力しています...")
        wait = WebDriverWait(self.driver, wait_time)
        input_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        input_field.clear()
        input_field.send_keys(text)
        time.sleep(1)
        logger.success(f"{selector} への入力が完了しました。")

    def upload_image(self, file_path: str, wait_time: int = 10):
        # 画像ファイルをアップロード
        logger.info(f"{file_path} をアップロードしています...")
        file_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        file_input.send_keys(file_path)
        time.sleep(2)
        logger.success(f"{file_path} のアップロードが完了しました。")

    def paste_content(self, selector: str, content: str, wait_time: int = 10):
        # 指定されたセレクタの要素に内容を追加
        logger.info(f"{selector} に内容を追加しています...")
        wait = WebDriverWait(self.driver, wait_time)
        editor = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        
        # 既存の内容を取得
        existing_content = self.driver.execute_script("return arguments[0].innerHTML;", editor)
        
        # 新しい内容を既存の内容の後に追加
        updated_content = existing_content + content
        
        # 更新された内容を設定
        self.driver.execute_script(f"arguments[0].innerHTML = arguments[1];", editor, updated_content)
        
        time.sleep(1)
        logger.success(f"{selector} への内容の追加が完了しました。")

    def add_tags(self, tags: List[str], wait_time: int = 10):
        # タグを追加
        logger.info("タグを追加しています...")
        wait = WebDriverWait(self.driver, wait_time)
        tag_container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".rs__value-container")))
        
        ActionChains(self.driver).move_to_element(tag_container).click().perform()
        time.sleep(0.5)
                
        for tag in tags:
            try:
                ActionChains(self.driver).send_keys(tag).perform()
                time.sleep(3)
                
                ActionChains(self.driver).send_keys(Keys.ENTER).perform()
                time.sleep(3)
                
                logger.success(f"タグ '{tag}' を追加しました。")
            except Exception as e:
                logger.error(f"タグ '{tag}' の追加に失敗しました: {str(e)}")
        
        logger.success("タグの追加処理が完了しました。")

    def close_driver(self):
        # WebDriverを閉じる
        if self.driver:
            logger.info("WebDriverを閉じています...")
            self.driver.quit()
            logger.success("WebDriverを閉じました。")

    def create_article(self, headless: bool = False, draft_url: Optional[str] = None, 
                       title: str = "Seleniumで自動投稿するテスト記事", 
                       content_file: str = 'content.md', 
                       content_md: str = None, 
                       image_file: Optional[str] = None, 
                       tags: List[str] = ["Python", "Selenium", "自動化"]):
        # 記事を作成または編集
        tprint('>>  ZennAPI')
        try:
            self.initialize_driver(headless)
            
            if draft_url:
                # 下書き記事を編集する場合
                self.navigate_to_url(draft_url)
            else:
                # 新規記事を作成する場合
                self.navigate_to_url("https://zenn.dev/")
                self.click_button(".AddNewMenu_buttonAddNew__mEP_v")
                self.click_button("button.AddNewMenu_panelItem__TzNBC")
                self.fill_text_input(".FullSizeEditor_titleField__SIUOR", title)
            
            # 画像ファイルが指定されている場合はアップロード
            if image_file:
                # 相対パスを絶対パスに変換
                absolute_image_path = os.path.abspath(image_file)
                if os.path.exists(absolute_image_path):
                    self.upload_image(absolute_image_path)
                else:
                    logger.error(f"指定された画像ファイルが見つかりません: {absolute_image_path}")
                    
            # 記事の内容を読み込んで貼り付け
            if(content_md):
                content = content_md
            else:
                with open(content_file, 'r', encoding='utf-8') as file:
                    content = file.read()
            self.paste_content(".cm-content", content)
            
            
            # 設定画面を開く
            self.click_button(".View_buttonIconSettings___roWJ")
            
            # タグを追加
            self.add_tags(tags)
            
            # 保存ボタンをクリック
            self.click_button(".Button_primary__VcoA9")
            logger.success("記事を保存しました。")
            
        finally:
            # WebDriverを閉じる（必要に応じてコメントアウトを解除）
            self.close_driver()
            pass


if __name__ == "__main__":
    # ZennAPIのインスタンスを作成
    zenn_api = ZennAPI(
        firefox_binary_path="C:\\Program Files\\Mozilla Firefox\\firefox.exe",
        firefox_profile_path="C:\\Users\\makim\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\c8ur3g2w.default-release"
    )
    
    # 記事を作成または編集
    zenn_api.create_article(
        title="Seleniumを使用したZenn記事の自動投稿",
        content_file="memo.md",
        image_file="C:\\Users\\makim\\Downloads\\WP_Mer.png",
        draft_url="https://zenn.dev/articles/59393e750570da/edit",
        tags=["Python", "Selenium", "自動化", "Zenn"]
    )
