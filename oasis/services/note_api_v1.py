from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from janome.tokenizer import Tokenizer

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import os

from markdown import markdown
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

from time import sleep
from random import randint
import builtins
import re
from loguru import logger
from tqdm import tqdm

class NoteAPI:
    def __init__(self, email: str, password: str, user_id: str, firefox_binary_path=None, firefox_profile_path=None):
        '''
        Noteアカウントのメールアドレスとパスワードを設定します
        '''
        self.email = email
        self.password = password
        self.user_id = user_id
        self.firefox_binary_path = firefox_binary_path
        self.firefox_profile_path = firefox_profile_path

    def __str__(self):
        return f"Email : {self.email} / User ID : {self.user_id}"

    def _init_driver(self, headless: bool = False):
        """WebDriverを初期化して返します。

        Args:
            headless (bool, optional): ヘッドレスモードで起動するかどうか. Defaults to False.

        Returns:
            webdriver.Firefox: 初期化されたWebDriverインスタンス
        """
        logger.info("WebDriverを初期化しています...")

        options = Options()
        if headless:
            options.add_argument("--headless")

        # ユーザーエージェントを正しく設定
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        options.set_preference("general.useragent.override", user_agent)

        # インスタンス変数から Firefox のパスを取得、設定されていない場合は環境変数から取得
        firefox_binary = self.firefox_binary_path or os.getenv('FIREFOX_BINARY_PATH')
        if firefox_binary:
            options.binary_location = firefox_binary

        # インスタンス変数から Firefox のプロファイルパスを取得、設定されていない場合は環境変数から取得
        profile_path = self.firefox_profile_path or os.getenv('FIREFOX_PROFILE_PATH')
        if profile_path:
            options.add_argument(f'-profile {profile_path}')

        logger.debug(f"profile_path : {profile_path}")
        logger.debug(f"firefox_binary : {firefox_binary}")

        # GeckoDriverManagerを使用してドライバーを自動的にダウンロードし管理
        service = Service(GeckoDriverManager().install())

        driver = webdriver.Firefox(service=service, options=options)

        # ウィンドウサイズを設定
        driver.set_window_size(1920, 1080)

        logger.success("WebDriverの初期化が完了しました。")
        return driver
    
    def _login(self, driver: webdriver.Firefox):
        """Noteにログインします。

        Args:
            driver (webdriver.Firefox): WebDriverインスタンス
        """
        try:
            logger.info("Noteにログインしています...")
            driver.get('https://note.com/login?redirectPath=%2Fnotes%2Fnew')

            wait = WebDriverWait(driver, 10)

            sleep(5)
            email_input = wait.until(EC.presence_of_element_located((By.ID, 'email')))
            email_input.send_keys(self.email)
            sleep(0.5)
            password_input = wait.until(EC.presence_of_element_located((By.ID, 'password')))
            password_input.send_keys(self.password)
            sleep(0.5)
            login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".o-login__button button")))
            login_button.click()
            sleep(2)
            
        except:
            logger.info("Noteに自動ログインしました...")
            driver.get('https://editor.note.com/new')
            wait = WebDriverWait(driver, 10)
            sleep(2)
            
        logger.success("Noteへのログインが完了しました。")

    def _input_title(self, driver: webdriver.Firefox, title: str):
        """記事のタイトルを入力します。

        Args:
            driver (webdriver.Firefox): WebDriverインスタンス
            title (str): 記事のタイトル
        """
        logger.info("記事のタイトルを入力しています...")
        textarea = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
        textarea.click()
        textarea.send_keys(title)
        textarea.send_keys(Keys.ENTER)
        logger.success("記事のタイトル入力が完了しました。")

    def _load_text_content(self, file_name: str = None, text: str = None) -> str:
        """記事コンテンツをファイルまたはテキストから読み込みます。

        Args:
            file_name (str, optional): 記事コンテンツファイル名. Defaults to None.
            text (str, optional): 記事コンテンツテキスト. Defaults to None.

        Returns:
            str: 記事コンテンツ
        """
        logger.info("記事コンテンツを読み込んでいます...")
        if text is None:
            with open(file=file_name, mode='r', encoding='utf-8') as f:
                text = f.read()
        logger.success("記事コンテンツの読み込みが完了しました。")
        return text

    def _input_text(self, driver: webdriver.Firefox, text: str):
        """記事の本文を入力します。

        Args:
            driver (webdriver.Firefox): WebDriverインスタンス
            text (str): 記事の本文
        """
        logger.info("記事の本文を入力しています...")
        edit_text = text.split('\n')

        url = re.compile(r'https?://')
        pattern = re.compile(r'^\d+\. ')
        minusgt = re.compile(r'^[\->] ')
        blockquote = False
        code_block = []  # コードブロックの内容を保存するリスト

        for i, text in enumerate(tqdm(edit_text, desc="本文入力中")):
            active_element = driver.execute_script("return document.activeElement;")  # active_elementを取得

            if "```" in text:
                blockquote = self._toggle_blockquote(active_element, blockquote, code_block)
                if not blockquote:
                    self._input_code_block(driver, code_block)
                    code_block = []
            else:
                if blockquote:
                    code_block.append(text)
                else:
                    blockquote = self._process_text_line(driver, text, i, edit_text, url, pattern, minusgt, blockquote)

        logger.success("記事の本文入力が完了しました。")

    def _input_code_block(self, driver: webdriver.Firefox, code_block: list):
        """コードブロックの内容を一括して入力します。

        Args:
            driver (webdriver.Firefox): WebDriverインスタンス
            code_block (list): コードブロックの内容を保存するリスト
        """
        if code_block:
            code_text = '\n'.join(code_block)
            active_element = driver.execute_script("return document.activeElement;")
            active_element.send_keys(code_text)
            sleep(0.5)
            active_element.send_keys(Keys.ENTER)
            # active_element.send_keys('```')
            sleep(0.5)
            active_element.send_keys(Keys.ENTER)


    def _process_text_line(self, driver: webdriver.Firefox, text: str, i: int, edit_text: list, url, pattern, minusgt, blockquote: bool):
        """1行のテキスト処理を行い、WebDriverに入力します。

        Args:
            driver (webdriver.Firefox): WebDriverインスタンス
            text (str): 処理対象のテキスト行
            i (int): 現在の行番号
            edit_text (list): 全体のテキスト行リスト
            url: URLパターン
            pattern: 番号付きリストパターン
            minusgt: マイナス記号または大記号で始まるリストパターン
            blockquote (bool): 引用符ブロック内かどうか
        """
        active_element = driver.execute_script("return document.activeElement;")
        if text.startswith('#### '):
            text = f"**{text}**".replace("#### ", "")

        if text.startswith('### '):
            self._input_heading(active_element, i, edit_text, text, 3)
        elif text.startswith('## '):
            self._input_heading(active_element, i, edit_text, text, 2)
        elif pattern.search(text):
            self._input_ordered_list(active_element, text, i, edit_text, pattern)
        elif text == "---":
            self._input_horizontal_rule(active_element)
        elif text == '':
            self._input_empty_line(active_element, i, edit_text, blockquote)
        elif url.search(text):
            self._input_url(driver, active_element, text, i, edit_text)
        elif "```" in text:
            blockquote = self._toggle_blockquote(active_element, blockquote)
        elif minusgt.search(text):
            self._input_unordered_list(active_element, text, i, edit_text, minusgt)
        else:
            self._input_plain_text(active_element, text, i, edit_text)

        return blockquote

    def _input_heading(self, active_element, i, edit_text, text: str, level: int):
        """見出しを入力します。

        Args:
            active_element: アクティブな要素
            text (str): 見出しテキスト
            level (int): 見出しレベル (2 or 3)
        """
        
        front_line = edit_text[i - 1]
        logger.debug(f'front_line: {front_line}')
        if front_line.startswith(('## ', '-', '>', '1. ')):
            sleep(0.5)
            
        # sleep(0.5)
        # active_element.send_keys(Keys.ENTER)
        sleep(0.5)
        active_element.send_keys(f'{"#" * level}')
        sleep(0.5)
        active_element.send_keys(Keys.SPACE)
        sleep(0.5)
        active_element.send_keys(text.replace(f'{"#" * level} ', ''))
        sleep(0.5)
        active_element.send_keys(Keys.ENTER)

    def _input_ordered_list(self, active_element, text: str, i: int, edit_text: list, pattern):
        """番号付きリストを入力します。

        Args:
            active_element: アクティブな要素
            text (str): リストアイテムテキスト
            i (int): 現在の行番号
            edit_text (list): 全体のテキスト行リスト
            pattern: 番号付きリストパターン
        """
        number = text[0]
        if pattern.search(edit_text[i - 1]):
            sleep(0.5)
            logger.debug(f'order text: {text}')
            self._input_text_with_format(active_element, text.replace(f'{number}. ', ''))
        else:
            logger.debug(f'order number: {number}')
            logger.debug(f'order text: {text}')
            sleep(0.5)
            active_element.send_keys(f'{number}.')
            sleep(0.5)
            active_element.send_keys(Keys.SPACE)
            sleep(0.5)
            self._input_text_with_format(active_element, text.replace(f'{number}. ', ''))
        self._insert_line_break_if_needed(active_element, i, edit_text, pattern)


    def _input_text_with_format(self, active_element, text: str):
        """太字、アンダーバーの置換、テキスト入力処理を行います。

        Args:
            active_element: アクティブな要素
            text (str): 入力するテキスト
        """
        text = re.sub(r'`([^`]*)`', r'**\1**', text)
        text = text.replace("_", "-")
        parts = re.split(r'(\*\*[^\*]*\*\*)', text)
        for part in parts:
            if re.match(r'\*\*[^\*]*\*\*', part):
                active_element.send_keys(part)  # アスタリスクを取り除いて入力
                logger.debug(f"text part: {part}")
                active_element.send_keys(Keys.SPACE)
            else:
                logger.debug(f"plane text: {part}")
                active_element.send_keys(part)

    def _input_horizontal_rule(self, active_element):
        """水平線を挿入します。

        Args:
            active_element: アクティブな要素
        """
        sleep(0.5)
        active_element.send_keys(Keys.ENTER)
        sleep(0.5)
        active_element.send_keys('---')

    def _input_empty_line(self, active_element, i: int, edit_text: list, blockquote: bool):
        """空行を挿入します。

        Args:
            active_element: アクティブな要素
            i (int): 現在の行番号
            edit_text (list): 全体のテキスト行リスト
            blockquote (bool): 引用符ブロック内かどうか
        """
        if blockquote:
            sleep(0.5)
            active_element.send_keys(' ')
        try:
            
            pre_line = edit_text[i - 1]
            next_line = edit_text[i + 1]
            logger.debug(f'pre_line: {pre_line}')
            logger.debug(f'next_line: {next_line}')

            logger.debug('--- Keys.ENTER ---')
            active_element.send_keys(Keys.ENTER)
            
            if pre_line.startswith(('-', '>', '1. ')) and next_line.startswith(('#### ', '### ', '## ')):
                sleep(0.5)
                logger.debug('--- Keys.ENTER ---')
                active_element.send_keys(Keys.ENTER)

        except:
            return

    def _input_url(self, driver, active_element, text: str, i: int, edit_text: list):
        """URLを入力し、マークダウンをHTMLに変換して挿入します。

        Args:
            driver: WebDriverインスタンス
            active_element: アクティブな要素
            text (str): マークダウンテキスト
            i (int): 現在の行番号
            edit_text (list): 全体のテキスト行リスト
        """
        # ツイッターのblockquoteがあるか確認
        blockquote_match = re.search(r'<blockquote class="twitter-tweet".*?<a href="(https://twitter\.com/.*?/status/\d+\?ref_src=twsrc%5Etfw)".*?</blockquote>', text, re.DOTALL)
        
        if blockquote_match:
            # ステータスのURLを抽出
            url = blockquote_match.group(1)
            text = url  # textをURLで置き換え
        
        # 以下、既存のコード（変更なし）
        match = re.search(r'\[(.*?)\]\((.*?)\)', text)
        
        if match:
            link_text, url = match.groups()
            html = markdown(text)
            
            soup = BeautifulSoup(html, 'html.parser')
            formatted_html = soup.prettify()
            
            logger.debug(f"text: {text}")
            logger.debug(f"html: {formatted_html}")
            
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
            driver.execute_script(script, active_element, formatted_html)

            sleep(0.5)
            return
        else:
            for char in text:
                active_element.send_keys(char)
                sleep(0.1)
            active_element.send_keys(Keys.ENTER)
            return
        

    def _toggle_blockquote(self, active_element, blockquote: bool, code_block: list) -> bool:
        """引用符ブロックを開始/終了します。

        Args:
            active_element: アクティブな要素
            blockquote (bool): 現在の引用符ブロック状態
            code_block (list): コードブロックの内容を保存するリスト

        Returns:
            bool: 反転した引用符ブロック状態
        """
        if blockquote:
            logger.debug(f">> コードブロック終了")
            sleep(0.5)
            active_element.send_keys(Keys.ENTER)
            return False
        else:
            logger.debug(f">> コードブロック開始")
            sleep(0.5)
            active_element.send_keys(Keys.ENTER)
            active_element.send_keys('```')
            return True

    def _input_unordered_list(self, active_element, text: str, i: int, edit_text: list, minusgt):
        """番号なしリストを入力します。

        Args:
            active_element: アクティブな要素
            text (str): リストアイテムテキスト
            i (int): 現在の行番号
            edit_text (list): 全体のテキスト行リスト
            minusgt: マイナス記号または大記号で始まるリストパターン
        """
        mark = text[0]
        markspace = f"{mark} "
        if edit_text[i - 1].startswith(markspace):
            sleep(0.5)
            self._input_text_with_format(active_element, text.replace(mark, ''))
        else:
            sleep(0.5)
            active_element.send_keys(mark)
            sleep(0.5)
            active_element.send_keys(Keys.SPACE)
            sleep(0.5)
            self._input_text_with_format(active_element, text.replace(mark, ''))
        self._insert_line_break_if_needed(active_element, i, edit_text, minusgt)

    def _input_plain_text(self, active_element, text: str, i: int, edit_text: list):
        """プレーンテキストを入力します。

        Args:
            active_element: アクティブな要素
            text (str): プレーンテキスト
            i (int): 現在の行番号
            edit_text (list): 全体のテキスト行リスト
        """
        sleep(0.1)
        self._input_text_with_format(active_element, text)
        sleep(0.1)
        active_element.send_keys(Keys.ENTER)
        
        try:
            if edit_text[i + 1].startswith(('## ', '-', '>', '1. ')):
                sleep(0.5)
                active_element.send_keys(Keys.ENTER)
        except:
            return
        
    def _insert_line_break_if_needed(self, active_element, i: int, edit_text: list, pattern):
        """リストアイテムの区切りに改行を挿入します。

        Args:
            active_element: アクティブな要素
            i (int): 現在の行番号
            edit_text (list): 全体のテキスト行リスト
            pattern: リストパターン
        """
        try:
            if pattern.search(edit_text[i + 1]):
                sleep(0.5)
                active_element.send_keys(Keys.ENTER)
                logger.debug(f"箇条書き中...")
            else:
                logger.debug(f"箇条書き終了")
                sleep(0.5)
                active_element.send_keys(Keys.ENTER)
                sleep(0.5)
                active_element.send_keys(Keys.ENTER)
        except:
            sleep(0.5)
            active_element.send_keys(Keys.ENTER)
            sleep(0.5)
            active_element.send_keys(Keys.ENTER)
    
    def _scroll_page(self, driver: webdriver.Firefox):
        """ページをスクロールします。

        Args:
            driver (webdriver.Firefox): WebDriverインスタンス
        """
        logger.info("ページをスクロールしています...")
        sleep(0.5)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        driver.execute_script('window.scrollTo(0, 0)')
        sleep(1)
        logger.success("ページのスクロールが完了しました。")

    def _extract_search_word(self, title: str) -> str:
        """タイトルから検索キーワードを抽出します。

        Args:
            title (str): 記事のタイトル

        Returns:
            str: 検索キーワード
        """
        logger.info("検索キーワードを抽出しています...")
        t = Tokenizer()
        keywords = [token.surface for token in t.tokenize(title) if token.part_of_speech.startswith(('名詞,一般', '名詞,固有名詞', '名詞,サ変接続'))]
        search_word = builtins.max(keywords, key=len) if keywords else None
        logger.success(f"検索キーワード '{search_word}' を抽出しました。")
        return search_word

    def _set_thumbnail(self, driver: webdriver.Firefox, wait: WebDriverWait, search_word: str, image_index: int or str):
        """サムネイル画像を設定します。"""
        logger.info("サムネイル画像を設定しています...")
        sleep(2)
        button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/main/div[1]/button")))
        logger.debug(f"button: {button}")  # ボタンのテキストをデバッグ出力
        button.click()

        sleep(2)
        button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/main/div[1]/div/div[2]/button")))
        logger.debug(f"button: {button}")  # ボタンのテキストをデバッグ出力
        button.click()

        sleep(2)
        button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div/div/div[1]/div/div[2]/button")))
        button.click()
        sleep(2)
        keyword_input = driver.execute_script("return document.activeElement;")
        keyword_input.send_keys("illust sample")
        sleep(3)
        button = driver.find_element(By.XPATH, "/html/body/div[5]/div/div/div[1]/div/div[2]/button")
        button.click()
        sleep(3)
        parent_element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div/div/div[2]")))
        img_elements = parent_element.find_elements(By.TAG_NAME, 'img')
        
        index = self._select_image_index(image_index, img_elements)
        
        if index < 0 or isinstance(image_index, type(None)):
            keyword_input.send_keys(Keys.ESCAPE)
        else:
            img_elements[index].click()
            button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div/div/div[2]/div/div[2]/div/div[5]/button[2]")))
            button.click()
            sleep(5)
            button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div/div/div[3]/button[2]")))
            button.click()
            sleep(20)
        logger.success("サムネイル画像の設定が完了しました。")

    def _select_image_index(self, image_index: int or str, img_elements: list) -> int:
        """画像のインデックスを選択します。

        Args:
            image_index (int or str): 画像インデックス (random, None, またはインデックス番号)
            img_elements (list): 画像要素のリスト

        Returns:
            int: 選択された画像インデックス
        """
        if isinstance(image_index, int) and 0 <= int(image_index) <= int(len(img_elements) - 1):
            return image_index
        elif image_index == 'random':
            max_index = len(img_elements) - 1
            return randint(0, max_index) if max_index >= 0 else -1
        else:
            return -1

    def _set_tags(self, driver: webdriver.Firefox, wait: WebDriverWait, input_tag_list: list):
        """タグを設定します。"""
        logger.info("タグを設定しています...")
        sleep(1)
        input_element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[1]/div[2]/main/section[1]/div[2]/div/div[1]/input')))
        input_element.click()
        sleep(0.5)
        input = driver.execute_script("return document.activeElement;")
        for tag in input_tag_list:
            sleep(0.5)
            logger.debug(f"tag : [{tag}]")
            input.send_keys(tag.replace(" ", "").replace(".", ""))
            sleep(0.5)
            input = driver.execute_script("return document.activeElement;")
            input.send_keys(Keys.SPACE)
        logger.success("タグの設定が完了しました。")


    def _publish_article(self, driver: webdriver.Firefox, wait: WebDriverWait, input_tag_list : list) -> dict:
        """記事を公開します。"""
        logger.info("記事を公開しています...")
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/header/div/div[2]/div/button[2]")))
        button.click()
        sleep(2)
        
        # タグ設定処理を呼び出す
        self._set_tags(driver, wait, input_tag_list)

        button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[1]/div/button")))
        button.click()

        url = driver.current_url
        cut_url = url.split('/')
        post_id = cut_url[4]
        post_url = f'https://note.com/{self.user_id}/n/{post_id}'

        logger.success(f"記事が公開されました。URL: {post_url}")
        return {
            'run': 'success',
            'post_setting': 'Public',
            'post_url': post_url
        }

    def _save_draft(self, driver: webdriver.Firefox, wait: WebDriverWait) -> dict:
        """記事を下書き保存します。"""
        logger.info("記事を下書き保存しています...")
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[2]/div[1]/header/div/div[2]/div/button[1]")))
        button.click()
        logger.success("記事が下書き保存されました。")
        return {
            'run': 'success',
            'post_setting': 'Draft',
        }

    def create_article(self, title: str, input_tag_list: list, image_index='random', post_setting: bool = False, file_name: str = None, headless: bool = True, text: str = None) -> dict:
        '''
        新規記事を作成します。

        Args:
            title (str): 記事のタイトル
            input_tag_list (list): 記事のタグリスト
            image_index (str or int, optional): 記事画像のインデックス番号 (random, None, またはインデックス番号). Defaults to 'random'.
            post_setting (bool, optional): 下書き保存するか公開するか (デフォルトは下書き保存). Defaults to False.
            file_name (str, optional): 記事コンテンツファイル名. Defaults to None.
            headless (bool, optional): ヘッドレスモードで起動するかどうか. Defaults to True.
            text (str, optional): 記事コンテンツテキスト. Defaults to None.

        Returns:
            dict: 実行結果
        '''
        logger.info("記事の作成を開始します...")
        if not all([title, input_tag_list, isinstance(input_tag_list, list), 
                    (image_index == 'random' or isinstance(image_index, (int, type(None)))), 
                    (file_name is not None or text is not None)]):
            logger.error("必須データがありません。")
            return {'run': 'error', 'message': '必須データがありません。'}
        
        driver = self._init_driver(headless)
        self._login(driver)
        self._input_title(driver, title)
        
        text = self._load_text_content(file_name, text)
        self._input_text(driver, text)
        
        self._scroll_page(driver)
        search_word = self._extract_search_word(title)
        
        wait = WebDriverWait(driver, 10)
        self._set_thumbnail(driver, wait, search_word, image_index)

        if post_setting:
            res = self._publish_article(driver, wait, input_tag_list )
        else:
            res = self._save_draft(driver, wait)

        res.update({'title': title, 'file_path': file_name, 'tag_list': input_tag_list})
        driver.quit()
        logger.success("📒 記事の作成が完了しました。")
        return res
