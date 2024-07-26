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
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException

import json

from PIL import Image
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

        
        
    def click_button(self, selector: str, by: By = By.XPATH, timeout: int = 10, retries: int = 3):
        logger.info(f"{selector} ボタンをクリックしています...")
        
        for attempt in range(retries):
            try:
                # 要素が見つかるまで待機
                element = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((by, selector))
                )
                
                # クリックを試みる
                element.click()
                
                # クリック後の短い待機
                time.sleep(2)
                
                logger.success(f"{selector} ボタンのクリックが完了しました。")
                return True  # クリック成功
            
            except (TimeoutException, ElementClickInterceptedException, StaleElementReferenceException) as e:
                logger.warning(f"クリック試行 {attempt + 1}/{retries} 失敗: {str(e)}")
                
                if attempt < retries - 1:
                    time.sleep(2)  # 次の試行前に少し待機
                else:
                    # 最後の試行でも失敗した場合
                    logger.error(f"{selector} ボタンのクリックに失敗しました。")
                    self.take_screenshot(f"click_error_{selector.replace('/', '_')}_{int(time.time())}.png")
                    return False  # クリック失敗
        
        return False  # すべての試行が失敗


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

    def convert_webp_to_png(self, file_path: str) -> str:
        if file_path.lower().endswith('.webp'):
            im = Image.open(file_path).convert("RGBA")
            png_path = os.path.splitext(file_path)[0] + ".png"
            im.save(png_path, "PNG")
            logger.info(f"WebPファイル {file_path} をPNGファイル {png_path} に変換しました。")
            return png_path
        return file_path

    def upload_image(self, file_path: str, wait_time: int = 10):
        
        # WebPファイルの場合、PNGに変換
        file_path = self.convert_webp_to_png(file_path)
        time.sleep(5)
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

    def click_create_post_button(self):
        xpath = "//span[contains(@class, 'x1lliihq') and .//span[text()='作成']]"
        return self.click_button(xpath, by=By.XPATH)

    def click_next_button(self):
        xpath = "//div[contains(@class, 'x9f619') and contains(@class, 'xjbqb8w') and text()='次へ']"
        return self.click_button(xpath, by=By.XPATH)

    def click_share_button(self):
        xpath = "//div[contains(@class, 'x9f619') and contains(@class, 'xjbqb8w') and text()='シェア']"
        return self.click_button(xpath, by=By.XPATH)

    def create_post(self, image_file: str, caption_file: str, headless: bool = False):
        # Instagram投稿を作成
        tprint('>>  InstaAPI')
        try:
            self.initialize_driver(headless)
            
            # ログイン（環境変数からユーザー名とパスワードを取得）
            self.login(os.getenv("INSTAGRAM_USERNAME"), os.getenv("INSTAGRAM_PASSWORD"))
            
            # 投稿ボタンをクリック
            xpath = "//span[contains(@class, 'x4k7w5x')]//a[contains(@class, '_a6hd')]"
            # self.click_button(xpath, by=By.XPATH)
            self.click_create_post_button()
            
            # 画像をアップロード
            self.upload_image(image_file)
            
            # 「次へ」ボタンを2回クリック
            # self.click_button("/html/body/div[6]/div[1]/div/div[3]/div/div/div/div/div/div/div/div[1]/div/div/div/div[3]/div", by=By.XPATH)
            self.click_next_button()
            time.sleep(2)
            self.click_next_button()
            # self.click_button("/html/body/div[6]/div[1]/div/div[3]/div/div/div/div/div/div/div/div[1]/div/div/div/div[3]/div", by=By.XPATH)
            
            # キャプションを入力
            with open(caption_file, 'r', encoding='utf-8') as file:
                caption = file.read()
            self.fill_text_input(".x1hnll1o", caption)
            
            time.sleep(2)
            # 投稿ボタンをクリック
            # self.click_button("/html/body/div[6]/div[1]/div/div[3]/div/div/div/div/div/div/div/div[1]/div/div/div/div[3]/div", by=By.XPATH)
            self.click_share_button()
            
            logger.success("投稿が完了しました。")
            time.sleep(20)
            
        finally:
            self.close_driver()

if __name__ == "__main__":
    # InstaAPIV1クラスのインスタンスを作成し、投稿を実行
    insta_api_v1 = InstaAPIV1(
        firefox_binary_path="C:\\Program Files\\Mozilla Firefox\\firefox.exe",
        firefox_profile_path="C:\\Users\\makim\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\q8b2lcl6.Yukihiko"
    )
    insta_api_v1.create_post(
        image_file=r"C:\Users\makim\Downloads\Yuki5.webp",
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
