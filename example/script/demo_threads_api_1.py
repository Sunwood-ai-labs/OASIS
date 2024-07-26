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
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import json
from PIL import Image

from loguru import logger
from art import *
from tqdm import tqdm
import random

class ThreadsAPIV1:
    def __init__(
        self,
        firefox_binary_path: Optional[str] = None,
        firefox_profile_path: Optional[str] = None,
    ):
        self.firefox_binary_path = firefox_binary_path
        self.firefox_profile_path = firefox_profile_path
        self.driver = None

    def initialize_driver(self, headless: bool = False):
        logger.info("WebDriverを初期化しています...")
        options = Options()
        # ユーザーエージェントの設定
        # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        if headless:
            options.add_argument("--headless")

        if self.firefox_binary_path:
            options.binary_location = self.firefox_binary_path
        elif os.getenv("FIREFOX_BINARY_PATH"):
            options.binary_location = os.getenv("FIREFOX_BINARY_PATH")

        if self.firefox_profile_path:
            options.profile = webdriver.FirefoxProfile(self.firefox_profile_path)
        elif os.getenv("FIREFOX_PROFILE_PATH"):
            options.profile = webdriver.FirefoxProfile(os.getenv("FIREFOX_PROFILE_PATH"))

        service = Service(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=service, options=options)
        self.driver.set_window_size(1920, 1080)
        logger.success("WebDriverの初期化が完了しました。")

    def login(self, username: str, password: str):
        logger.info("Threadsにログインしています...")
        self.navigate_to_url("https://www.threads.net/")
        time.sleep(2)
        # ログイン処理を追加する必要があります（Threadsの具体的なログイン手順に応じて）
        logger.success("ログインが完了しました。")

    def navigate_to_url(self, url: str):
        logger.info(f"{url} に移動しています...")
        self.driver.get(url)
        time.sleep(2)
        logger.success(f"{url} への移動が完了しました。")

    def click_button(self, selector: str, wait_time: int = 10, by: By = By.CSS_SELECTOR):
        logger.info(f"{selector} ボタンをクリックしています...")
        wait = WebDriverWait(self.driver, wait_time)
        button = wait.until(EC.element_to_be_clickable((by, selector)))
        button.click()
        time.sleep(1)
        logger.success(f"{selector} ボタンのクリックが完了しました。")

    def wait_for_element(self, locator: tuple, timeout: int = 20, poll_frequency: float = 0.5):
        wait = WebDriverWait(self.driver, timeout, poll_frequency=poll_frequency, ignored_exceptions=[StaleElementReferenceException])
        return wait.until(EC.presence_of_element_located(locator))

    def fill_text_input(self, selector: str, text: str, wait_time: int = 10, chunk_size: int = 10, delay: float = 0.1, by: By = By.CSS_SELECTOR):
        # テキスト入力フィールドにテキストを入力
        logger.info(f"{selector} に \n{text}\n を入力しています...")
        wait = WebDriverWait(self.driver, wait_time)
        input_field = wait.until(EC.presence_of_element_located((by, selector)))
        
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
        
        # WebPファイルの場合、PNGに変換
        file_path = self.convert_webp_to_png(file_path)
        
        logger.info(f"{file_path} をアップロードしています...")
        file_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        file_input.send_keys(file_path)
        time.sleep(2)
        logger.success(f"{file_path} のアップロードが完了しました。")

    def close_driver(self):
        if self.driver:
            logger.info("WebDriverを閉じています...")
            self.driver.quit()
            logger.success("WebDriverを閉じました。")

    def convert_webp_to_png(self, file_path: str) -> str:
        if file_path.lower().endswith('.webp'):
            im = Image.open(file_path).convert("RGBA")
            png_path = os.path.splitext(file_path)[0] + ".png"
            im.save(png_path, "PNG")
            logger.info(f"WebPファイル {file_path} をPNGファイル {png_path} に変換しました。")
            return png_path
        return file_path

    def create_post(self, image_file: str, caption_file: str, headless: bool = False):
        tprint('>>  ThreadsAPI')
        try:
            self.initialize_driver(headless)
            
            self.login(os.getenv("THREADS_USERNAME"), os.getenv("THREADS_PASSWORD"))
            
            # 投稿ボタンをクリック
            self.click_button("div.x4uap5:nth-child(3)")
            
            # キャプションを入力
            with open(caption_file, 'r', encoding='utf-8') as file:
                caption = file.read()
            
            time.sleep(2)
            # self.fill_text_input("/html/body/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[3]/div[1]/div[1]/p", caption)
            # self.fill_text_input("p.xdj266r", caption)
            # /html/body/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[3]/div[1]/div[1]
            # /html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[3]/div[1]/div[1]
            self.fill_text_input("/html/body/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[3]/div[1]/div[1]", caption, by=By.XPATH)
            
            # /html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[3]/div[1]/div/p
            # /html/body/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[3]/div[1]/div[1]/p
            # 画像をアップロード
            # self.click_button("div.xp7jhwk:nth-child(2) > div:nth-child(1)")
            self.upload_image(image_file)
            
            time.sleep(2)
            # 投稿ボタンをクリック
            self.click_button(".x15zctf7 > div:nth-child(1) > div:nth-child(1)")
            
            logger.success("投稿が完了しました。")
            time.sleep(20)
            
        finally:
            self.close_driver()

if __name__ == "__main__":
    threads_api_v1 = ThreadsAPIV1(
        firefox_binary_path="C:\\Program Files\\Mozilla Firefox\\firefox.exe",
        firefox_profile_path="C:\\Users\\makim\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\q8b2lcl6.Yukihiko"
    )
    threads_api_v1.create_post(
        image_file=r"C:\Users\makim\Downloads\Yuki5.webp",
        caption_file="sample.md"
    )
