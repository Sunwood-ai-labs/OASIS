from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import TimeoutException
from PIL import Image
import time
import os
from selenium.webdriver.common.action_chains import ActionChains
from loguru import logger
import random

logger.add("instagram_automation.log", rotation="500 MB")


# GeckoDriverのパスを指定
geckodriver_path = r"C:\Program Files\geckodriver-v0.35.0-win32\geckodriver.exe"


class InstaAPIV1:
    def __init__(self, firefox_binary_path=None, firefox_profile_path=None):
        self.firefox_binary_path = firefox_binary_path
        self.firefox_profile_path = firefox_profile_path
        self.driver = None

    def initialize_driver(self):
        logger.info("ドライバーの初期化を開始します")
        options = Options()
        if self.firefox_binary_path:
            options.binary_location = self.firefox_binary_path
        if self.firefox_profile_path:
            options.profile = webdriver.FirefoxProfile(self.firefox_profile_path)
        
        service = Service(geckodriver_path)
        self.driver = webdriver.Firefox(service=service, options=options)
        self.driver.set_window_size(1920, 1280)  # より大きなサイズに設定
        logger.info("ドライバーの初期化が完了しました")

    def login(self, username, password):
        logger.info("ログイン処理を開始します")
        self.driver.get("https://www.instagram.com/")
        time.sleep(2)
        # ログイン処理を実装（ユーザー名とパスワードの入力、ログインボタンのクリックなど）
        logger.info("ログインが完了しました")

    def click_element(self, selectors, element_type="*", timeout=30):
        logger.info(f"要素 '{selectors}' をクリックしようとしています")
        def find_clickable_element(driver):
            for selector in selectors:
                if element_type == "xpath":
                    elements = driver.find_elements(By.XPATH, selector)
                else:
                    elements = driver.find_elements(By.XPATH, f"//{element_type}[contains(text(), '{selector}')]") + \
                            driver.find_elements(By.XPATH, f"//{element_type}[contains(@aria-label, '{selector}')]")
                
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        return element
            return False

        try:
            element = WebDriverWait(self.driver, timeout).until(find_clickable_element)
            actions = ActionChains(self.driver)
            actions.move_to_element(element).click().perform()
            logger.info(f"要素 '{selectors}' をクリックしました")
            return
        except TimeoutException:
            logger.warning(f"要素 '{selectors}' が見つかりません。JavaScriptクリックを試みます")
        
        # JavaScript click as a fallback
        for selector in selectors:
            if element_type == "xpath":
                script = f"""
                    var element = document.evaluate("{selector}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    if (element && element.offsetWidth > 0 && element.offsetHeight > 0) {{
                        element.click();
                        return true;
                    }}
                    return false;
                """
            else:
                script = f"""
                    var elements = document.evaluate("//*[contains(text(), '{selector}') or contains(@aria-label, '{selector}')]", document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null);
                    for (var i = 0; i < elements.snapshotLength; i++) {{
                        var element = elements.snapshotItem(i);
                        if (element.offsetWidth > 0 && element.offsetHeight > 0) {{
                            element.click();
                            return true;
                        }}
                    }}
                    return false;
                """
            clicked = self.driver.execute_script(script)
            if clicked:
                logger.info(f"JavaScriptを使用して要素 '{selector}' をクリックしました")
                return

        logger.error(f"要素 '{selectors}' が見つからないか、クリックできません")
        raise Exception(f"Element with selectors {selectors} not found or not clickable")

    def click_crop_button(self):
        logger.info("切り取りを選択ボタンをクリックしようとしています")
        try:
            crop_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, '_acan') and contains(@class, '_acao') and contains(@class, '_acas') and contains(@class, '_aj1-') and contains(@class, '_ap30')]//svg[@aria-label='切り取りを選択']"))
            )
            crop_button.click()
            logger.info("切り取りを選択ボタンをクリックしました")
        except TimeoutException:
            logger.warning("切り取りを選択ボタンが見つかりません。JavaScriptクリックを試みます")
            script = """
                var buttons = document.querySelectorAll('button._acan._acao._acas._aj1-._ap30');
                for (var button of buttons) {
                    if (button.querySelector('svg[aria-label="切り取りを選択"]')) {
                        button.click();
                        return true;
                    }
                }
                return false;
            """
            clicked = self.driver.execute_script(script)
            if clicked:
                logger.info("JavaScriptを使用して切り取りを選択ボタンをクリックしました")
            else:
                logger.error("切り取りを選択ボタンが見つからないか、クリックできません")
                raise Exception("切り取りを選択ボタンが見つからないか、クリックできません")

    def click_manage_button(self):
        logger.info("管理ボタンをクリックしようとしています")
        try:
            manage_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='管理' and @class='_aakl' and @role='button']"))
            )
            manage_button.click()
            logger.info("管理ボタンをクリックしました")
        except TimeoutException:
            logger.warning("管理ボタンが見つかりません。JavaScriptクリックを試みます")
            script = """
                var manageButton = document.querySelector('div[aria-label="管理"][class="_aakl"][role="button"]');
                if (manageButton) {
                    manageButton.click();
                    return true;
                }
                return false;
            """
            clicked = self.driver.execute_script(script)
            if clicked:
                logger.info("JavaScriptを使用して管理ボタンをクリックしました")
            else:
                logger.error("管理ボタンが見つからないか、クリックできません")
                raise Exception("管理ボタンが見つからないか、クリックできません")

    def click_post_button(self):
        logger.info("投稿ボタンをクリックしようとしています")
        selectors = [
            "//div[contains(@class, 'x1pi30zi')]//span[contains(text(), '投稿')]",
            "//span[contains(@class, 'x1lliihq') and contains(text(), '投稿')]",
            "//div[contains(@class, 'x9f619')]//span[contains(text(), '投稿')]",
            "//div[contains(@class, 'x78zum5')]//span[contains(text(), '投稿')]"
        ]
        
        try:
            for selector in selectors:
                try:
                    post_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    post_button.click()
                    logger.info(f"投稿ボタンをクリックしました: {selector}")
                    return
                except TimeoutException:
                    continue
            
            # If all selectors fail, try JavaScript click
            logger.warning("通常の方法で投稿ボタンが見つかりません。JavaScriptクリックを試みます")
            script = """
                var buttons = document.evaluate("//span[contains(text(), '投稿')]", document, null, XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE, null);
                for (var i = 0; i < buttons.snapshotLength; i++) {
                    var button = buttons.snapshotItem(i);
                    if (button.offsetWidth > 0 && button.offsetHeight > 0) {
                        button.click();
                        return true;
                    }
                }
                return false;
            """
            clicked = self.driver.execute_script(script)
            if clicked:
                logger.info("JavaScriptを使用して投稿ボタンをクリックしました")
                return
            
            logger.error("投稿ボタンが見つからないか、クリックできません")
            raise Exception("投稿ボタンが見つからないか、クリックできません")
        except Exception as e:
            logger.error(f"投稿ボタンのクリック中にエラーが発生しました: {str(e)}")
            raise
        
    def upload_media(self, file_path):
        logger.info(f"メディアのアップロードを開始します: {file_path}")
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension == '.webp':
            png_path = file_path.rsplit('.', 1)[0] + ".png"
            Image.open(file_path).convert("RGBA").save(png_path, "PNG")
            file_path = png_path
            logger.info(f"WebP画像をPNGに変換しました: {png_path}")

        file_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        file_input.send_keys(file_path)
        time.sleep(5)  # 動画の場合、アップロードに時間がかかる可能性があるため、待機時間を増やす

        if file_extension in ['.mp4', '.mov', '.avi']:
            logger.info("動画のアップロードを待機中...")
            try:
                time.sleep(5)
                logger.info("動画のアップロードが完了しました")

                # OKボタンをクリック
                self.click_element(["OK"])
                logger.info("OKボタンをクリックしました")

                # 動画の比率ボタンをクリック
                self.click_crop_button()

                # 元の比率ボタンをクリック
                original_ratio_selectors = [
                    "//div[contains(@class, 'x9f619')]//span[contains(text(), '元の比率')]",
                    "//span[contains(text(), '元の比率')]",
                    "//div[contains(@class, 'x9f619') and .//span[contains(text(), '元の比率')]]",
                ]
                
                time.sleep(3)
                self.click_element(original_ratio_selectors, element_type="xpath")
                logger.info("元の比率ボタンをクリックしました")

            except TimeoutException:
                logger.warning("動画のアップロード完了メッセージが表示されませんでした。処理を続行します。")

        logger.info("メディアのアップロードが完了しました")


    def enter_caption(self, caption):
        logger.info("キャプションの入力を開始します")
        caption_input = self.driver.find_element(By.CSS_SELECTOR, "div[aria-label='キャプションを入力…']")
        
        for char in caption:
            caption_input.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))  # ランダムな遅延を追加
        
        logger.info("キャプションの入力が完了しました")

    def create_post(self, media_file, caption_file):
        logger.info("投稿の作成を開始します")
        self.initialize_driver()
        self.login(os.getenv("INSTAGRAM_USERNAME"), os.getenv("INSTAGRAM_PASSWORD"))

        # 作成ボタンをクリック
        self.click_element(["作成"])
        time.sleep(3)
        self.click_post_button()
        time.sleep(3)
        
        # メディアをアップロード
        self.upload_media(media_file)

        # 「次へ」ボタンを2回クリック
        time.sleep(2)
        self.click_element(["次へ", "Next"])
        time.sleep(2)
        self.click_element(["次へ", "Next"])
        time.sleep(2)

        # 管理ボタンをクリック
        self.click_manage_button()
        time.sleep(2)
        
        # キャプションを入力
        with open(caption_file, 'r', encoding='utf-8') as file:
            caption = file.read()
        self.enter_caption(caption)

        # 投稿ボタンをクリック
        self.click_element(["シェア", "Share", "Post"])

        time.sleep(30)
        logger.info("投稿プロセスが完了しました")

if __name__ == "__main__":
    logger.info("Instagram自動投稿スクリプトを開始します")
    insta_api = InstaAPIV1(
        firefox_binary_path="C:\\Program Files\\Mozilla Firefox\\firefox.exe",
        firefox_profile_path=r"C:\Users\makim\AppData\Roaming\Mozilla\Firefox\Profiles\xznlto8o.Maki"
        # firefox_profile_path=r"C:\Users\makim\AppData\Roaming\Mozilla\Firefox\Profiles\q8b2lcl6.Yukihiko"
    )
    
    insta_api.create_post(
        # media_file=r"C:\Users\makim\Videos\yuki.mp4",  # 画像または動画ファイルのパスを指定
        media_file=r"C:\Users\makim\Downloads\無題の動画 ‐ Clipchampで作成 (69).mp4",
        # media_file=r"C:\Users\makim\Downloads\無題の動画 ‐ Clipchampで作成 (72).mp4",     
        caption_file="sample.md"
    )
    
    logger.info("Instagram自動投稿スクリプトが完了しました")

# OKボタン
# <button class=" _acan _acap _acaq _acas _acav _aj1- _ap30" type="button">OK</button>

# 動画の比率
# <button class=" _acan _acao _acas _aj1- _ap30" type="button">
# <div class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1y1aw1k x1sxyh0 xwib8y2 xurb0ha x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x6s0dn4 x1oa3qoh xl56j7k"><svg aria-label="切り取りを選択" class="x1lliihq x1n2onr6 x9bdzbf" fill="currentColor" height="16" role="img" viewBox="0 0 24 24" width="16"><title>切り取りを選択</title><path d="M10 20H4v-6a1 1 0 0 0-2 0v7a1 1 0 0 0 1 1h7a1 1 0 0 0 0-2ZM20.999 2H14a1 1 0 0 0 0 2h5.999v6a1 1 0 0 0 2 0V3a1 1 0 0 0-1-1Z">
# </path></svg></div></button>

# 元の比率
# <div class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x16n37ib x150jy0e x1e558r4 x1n2onr6 x1plvlek xryxfnj x1iyjqo2 x2lwn1j xeuugli x1q0g3np xqjyukv x6s0dn4 x1oa3qoh x1nhvcw1"><div class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 x1plvlek xryxfnj x1iyjqo2 x2lwn1j xeuugli xdt5ytf xqjyukv x1cy8zhl x1oa3qoh x1nhvcw1"><span class="x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp x1s688f x1roi4f4 x1tu3fi x3x7a5m x10wh9bi x1wdrske x8viiok x18hxmgj" dir="auto" style="line-height: var(--base-line-clamp-line-height); --base-line-clamp-line-height: 18px;">元の比率</span></div><div class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh xz9dl7a xn6708d xsag5q8 x1ye3gou x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"><svg aria-label="写真の外枠アイコン" class="x1lliihq x1n2onr6 x1roi4f4" fill="currentColor" height="24" role="img" viewBox="0 0 24 24" width="24"><title>写真の外枠アイコン</title><path d="M6.549 5.013A1.557 1.557 0 1 0 8.106 6.57a1.557 1.557 0 0 0-1.557-1.557Z" fill-rule="evenodd"></path><path d="m2 18.605 3.901-3.9a.908.908 0 0 1 1.284 0l2.807 2.806a.908.908 0 0 0 1.283 0l5.534-5.534a.908.908 0 0 1 1.283 0l3.905 3.905" fill="none" stroke="currentColor" stroke-linejoin="round" stroke-width="2"></path><path d="M18.44 2.004A3.56 3.56 0 0 1 22 5.564h0v12.873a3.56 3.56 0 0 1-3.56 3.56H5.568a3.56 3.56 0 0 1-3.56-3.56V5.563a3.56 3.56 0 0 1 3.56-3.56Z" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg></div></div>
