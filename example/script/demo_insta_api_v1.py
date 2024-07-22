import time
import os
from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import json

from loguru import logger
from art import *
from tqdm import tqdm

class InstaAPIV1:
    def __init__(
        self,
        firefox_binary_path: Optional[str] = None,
        firefox_profile_path: Optional[str] = None,
    ):
        # Firefoxのバイナリとプロファイルのパスを初期化
        self.firefox_binary_path = firefox_binary_path
        self.firefox_profile_path = firefox_profile_path
        self.driver = None

    def initialize_driver(self, headless: bool = False):
        # Seleniumのウェブドライバーを初期化
        logger.info("WebDriverを初期化しています...")
        options = Options()
        if headless:
            options.add_argument("--headless")

        # Firefoxのバイナリパスを設定
        if self.firefox_binary_path:
            options.binary_location = self.firefox_binary_path
        elif os.getenv("FIREFOX_BINARY_PATH"):
            options.binary_location = os.getenv("FIREFOX_BINARY_PATH")

        # Firefoxのプロファイルを設定
        if self.firefox_profile_path:
            options.profile = webdriver.FirefoxProfile(self.firefox_profile_path)
        elif os.getenv("FIREFOX_PROFILE_PATH"):
            options.profile = webdriver.FirefoxProfile(os.getenv("FIREFOX_PROFILE_PATH"))

        # ドライバーをインストールして初期化
        service = Service(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=service, options=options)
        self.driver.set_window_size(1920, 1080)
        logger.success("WebDriverの初期化が完了しました。")

    def login(self, username: str, password: str):
        # Instagramにログイン
        logger.info("Instagramにログインしています...")
        self.navigate_to_url("https://www.instagram.com/")
        time.sleep(2)
        logger.success("ログインが完了しました。")

    def navigate_to_url(self, url: str):
        # 指定されたURLに移動
        logger.info(f"{url} に移動しています...")
        self.driver.get(url)
        time.sleep(2)
        logger.success(f"{url} への移動が完了しました。")

    def click_button(self, selector: str, wait_time: int = 10, by: By = By.CSS_SELECTOR):
        # 指定されたセレクターのボタンをクリック
        logger.info(f"{selector} ボタンをクリックしています...")
        wait = WebDriverWait(self.driver, wait_time)
        button = wait.until(EC.element_to_be_clickable((by, selector)))
        button.click()
        time.sleep(1)
        logger.success(f"{selector} ボタンのクリックが完了しました。")

    def fill_text_input(self, selector: str, text: str, wait_time: int = 10, chunk_size: int = 10, delay: float = 0.1):
        # テキスト入力フィールドにテキストを入力
        logger.info(f"{selector} に \n{text}\n を入力しています...")
        wait = WebDriverWait(self.driver, wait_time)
        input_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        
        # 入力フィールドをクリア
        input_field.clear()
        time.sleep(0.5)  # クリア後少し待機
        
        # チャンク単位で遅延を入れながら入力
        for i in tqdm(range(0, len(text), chunk_size)):
            chunk = text[i:i+chunk_size]
            for char in chunk:
                input_field.send_keys(char)
                time.sleep(delay)
            time.sleep(0.5)  # チャンク間の長めの待機
        
        # 入力後の反応を待つ
        time.sleep(1)
        
        logger.success(f"{selector} への入力が完了しました。")

    def upload_image(self, file_path: str, wait_time: int = 10):
        # 画像をアップロード
        logger.info(f"{file_path} をアップロードしています...")
        file_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        file_input.send_keys(file_path)
        time.sleep(2)
        logger.success(f"{file_path} のアップロードが完了しました。")

    def close_driver(self):
        # WebDriverを閉じる
        if self.driver:
            logger.info("WebDriverを閉じています...")
            self.driver.quit()
            logger.success("WebDriverを閉じました。")

    def create_post(self, image_file: str, caption_file: str, headless: bool = False):
        # Instagram投稿を作成
        tprint('>>  InstaAPI')
        try:
            self.initialize_driver(headless)
            
            # ログイン（環境変数からユーザー名とパスワードを取得）
            self.login(os.getenv("INSTAGRAM_USERNAME"), os.getenv("INSTAGRAM_PASSWORD"))
            
            # 投稿ボタンをクリック
            self.click_button("/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[7]/div/span/div/a/div", by=By.XPATH)
            
            # 画像をアップロード
            self.upload_image(image_file)
            
            # 「次へ」ボタンを2回クリック
            self.click_button("/html/body/div[6]/div[1]/div/div[3]/div/div/div/div/div/div/div/div[1]/div/div/div/div[3]/div", by=By.XPATH)
            time.sleep(2)
            self.click_button("/html/body/div[6]/div[1]/div/div[3]/div/div/div/div/div/div/div/div[1]/div/div/div/div[3]/div", by=By.XPATH)
            
            # キャプションを入力
            with open(caption_file, 'r', encoding='utf-8') as file:
                caption = file.read()
            self.fill_text_input(".x1hnll1o", caption)
            
            time.sleep(2)
            # 投稿ボタンをクリック
            self.click_button("/html/body/div[6]/div[1]/div/div[3]/div/div/div/div/div/div/div/div[1]/div/div/div/div[3]/div", by=By.XPATH)
            
            logger.success("投稿が完了しました。")
            time.sleep(20)
            
        finally:
            self.close_driver()

if __name__ == "__main__":
    # InstaAPIV1クラスのインスタンスを作成し、投稿を実行
    insta_api_v1 = InstaAPIV1(
        firefox_binary_path="C:\\Program Files\\Mozilla Firefox\\firefox.exe",
        firefox_profile_path="C:\\Users\\makim\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\mkeo2nsd.kazami"
    )
    insta_api_v1.create_post(
        image_file="C:\\Users\\makim\\Downloads\\sample2.png",
        caption_file="sample.md"
    )

# ログイン
# https://www.threads.net/

# 投稿ボタン
# div.x4uap5:nth-child(3)

# 画像アップロード
# div.xp7jhwk:nth-child(2) > div:nth-child(1)

# 投稿文の入力
# p.xdj266r

# 投稿
# .x15zctf7 > div:nth-child(1) > div:nth-child(1)
