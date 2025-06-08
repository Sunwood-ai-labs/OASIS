# oasis\services\wordpress_api.py
import requests
from art import *
import re
import markdown
from markdown.extensions import codehilite, fenced_code
import html2text
import html
import os
from bs4 import BeautifulSoup, Comment

import re
import markdown
from bs4 import BeautifulSoup
from loguru import logger


try:
    from ..logger import logger
    from ..exceptions import APIError
except:
    import os
    import sys

    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from logger import logger
    from exceptions import APIError
    
class WordPressAPI:
    def __init__(self, base_url, auth_user, auth_pass):
        if(base_url):
            self.base_url = base_url.rstrip('/')  # 末尾のスラッシュを削除
        self.auth = (auth_user, auth_pass)
        self.api_url = f"{self.base_url}/wp-json/wp/v2"
        

        # APIエンドポイントの可用性をチェック
        try:
            response = requests.get(self.api_url, auth=self.auth)
            # logger.info(f"API response: {response.status_code}, {response.text}")
            if response.status_code == 404:
                raise APIError(f"WordPress REST API エンドポイントが見つかりません。URL: {self.api_url}")
            elif response.status_code != 200:
                raise APIError(f"WordPress REST API へのアクセスに失敗しました。ステータスコード: {response.status_code}")
            logger.info(f"WordPress REST API エンドポイントに接続しました: {self.api_url}")
        except requests.RequestException as e:
            raise APIError(f"WordPress サイトへの接続に失敗しました: {str(e)}")
    def _get_all_items(self, endpoint):
        items = []
        page = 1
        while True:
            response = requests.get(f"{self.api_url}/{endpoint}", auth=self.auth, params={'per_page': 100, 'page': page})
            if response.status_code != 200:
                raise APIError(f"{endpoint}の取得に失敗しました。ステータスコード: {response.status_code}")
            page_items = response.json()
            if not page_items:
                break
            items.extend(page_items)
            if len(page_items) < 100:
                break
            page += 1
        return items

    def create_post(self, post):
        tprint('>>  WordPressAPI')
        
        # マークダウンのMermaidブロックをWordPress用に変換
        processed_content = convert_markdown_with_mermaid(post.content)

        try:
            payload = {
                'title': post.title,
                'content': processed_content,
                'status': 'draft',
                'slug': post.slug,
                'categories': [self._create_or_get_term(cat, 'categories') for cat in post.categories],
                'tags': [self._create_or_get_term(tag, 'tags') for tag in post.tags]
            }
            
            # logger.info(f"投稿のペイロード: {payload}")
            response = requests.post(f"{self.api_url}/posts", json=payload, auth=self.auth)
            
            if response.status_code != 201:
                logger.error(f"投稿の作成に失敗しました。ステータスコード: {response.status_code}")
                logger.error(f"レスポンス: {response.text}")
                raise APIError(f"投稿の作成に失敗しました。ステータスコード: {response.status_code}")
            
            logger.info("投稿が正常に作成されました。")
            return response.json()['id']
        except Exception as e:
            logger.error(f"投稿の作成中にエラーが発生しました: {str(e)}")
            raise APIError(f"投稿の作成に失敗しました: {str(e)}")

    def _create_or_get_term(self, term, taxonomy):
        endpoint = f"{self.api_url}/{taxonomy}"
        # logger.info(f"Term creation/retrieval endpoint: {endpoint}")
    
        # # 名前とスラッグで既存のカテゴリ/タグを検索
        # logger.debug(f"{endpoint}?search={term['name']}")
        search_response = requests.get(f"{endpoint}?search={term['name']}", auth=self.auth)
        # logger.info(f"Search response: {search_response.status_code}, {search_response.text}")
        if search_response.status_code == 200:
            existing_items = search_response.json()
            for item in existing_items:
                if item['name'].lower() == term['name'].lower() or item['slug'] == term['slug']:
                    logger.info(f"既存の{taxonomy} '{term['name']}' (slug: {term['slug']}) が見つかりました。")
                    return item['id']

        # 既存のアイテムが見つからない場合、新規作成を試みる
        data = {
            'name': term['name'],
            'slug': term['slug']
        }
        logger.debug(f"endpoint :{endpoint}")
        logger.debug(f"data     :{data}")
        create_response = requests.post(endpoint, json=data, auth=self.auth)
        # logger.info(f"Create response: {create_response.status_code}, {create_response.text}")
        if create_response.status_code == 201:
            logger.info(f"新しい{taxonomy} '{term['name']}' を作成しました。")
            return create_response.json()['id']
        elif create_response.status_code == 400:
            # 400エラーの場合、同名のカテゴリ/タグが既に存在する可能性がある
            logger.warning(f"{taxonomy} '{term['name']}' の作成に失敗しました。同名のアイテムが既に存在する可能性があります。")
            # 再度検索を試みる（API側で更新があった可能性があるため）
            search_again_response = requests.get(f"{endpoint}?search={term['name']}", auth=self.auth)
            logger.info(f"Search again response: {search_again_response.status_code}, {search_again_response.text}")
            if search_again_response.status_code == 200:
                search_results = search_again_response.json()
                for item in search_results:
                    if item['name'].lower() == term['name'].lower() or item['slug'] == term['slug']:
                        logger.info(f"既存の{taxonomy} '{term['name']}' が見つかりました。")
                        return item['id']
        
        logger.error(f"{taxonomy} '{term['name']}' の作成または取得に失敗しました。ステータスコード: {create_response.status_code}")
        logger.error(f"レスポンス: {create_response.text}")
        raise APIError(f"{taxonomy} '{term['name']}' の作成または取得に失敗しました。")

    def upload_thumbnail(self, post_id, image_path):
        try:
            with open(image_path, 'rb') as img:
                files = {'file': img}
                response = requests.post(f"{self.api_url}/media", files=files, auth=self.auth)
                if response.status_code != 201:
                    raise APIError(f"メディアのアップロードに失敗しました。ステータスコード: {response.status_code}")
                
                media_id = response.json()['id']
                update_response = requests.post(f"{self.api_url}/posts/{post_id}", json={'featured_media': media_id}, auth=self.auth)
                if update_response.status_code != 200:
                    raise APIError(f"サムネイルの設定に失敗しました。ステータスコード: {update_response.status_code}")
                
                logger.info(f"サムネイルが正常にアップロードされ、投稿 {post_id} に設定されました。")
        except Exception as e:
            logger.error(f"サムネイルのアップロード中にエラーが発生しました: {str(e)}")
            raise APIError(f"サムネイルのアップロードに失敗しました: {str(e)}")

    def get_existing_categories_and_tags(self):
        try:
            categories = self._get_all_items('categories')
            tags = self._get_all_items('tags')

            category_map = {cat['name']: cat['id'] for cat in categories}
            tag_map = {tag['name']: tag['id'] for tag in tags}

            logger.info(f"{len(category_map)}個のカテゴリと{len(tag_map)}個のタグを取得しました。")
            return category_map, tag_map
        except Exception as e:
            logger.error(f"カテゴリとタグの取得中にエラーが発生しました: {str(e)}")
            raise APIError(f"カテゴリとタグの取得に失敗しました: {str(e)}")

    def _get_all_items(self, endpoint):
        items = []
        page = 1
        per_page = 100
        while True:
            response = requests.get(f"{self.api_url}/{endpoint}", auth=self.auth, params={'per_page': per_page, 'page': page})
            if response.status_code != 200:
                raise APIError(f"{endpoint}の取得に失敗しました。ステータスコード: {response.status_code}")
            page_items = response.json()
            if not page_items:
                break
            items.extend(page_items)
            if len(page_items) < per_page:
                break
            page += 1
        return items

def should_skip_code_block(code_content):
    """
    コードブロックをスキップすべきかどうかを判定する
    
    Args:
        code_content (str): コードブロックの内容
        
    Returns:
        bool: スキップすべき場合はTrue
    """
    if not code_content or not code_content.strip():
        return True
    
    content = code_content.strip()
    
    # 非常に短いコンテンツ（3文字未満）
    if len(content) < 3:
        return True
    
    # 単一のファイル拡張子（例: .qmd, .py, .js など）
    if len(content.split('\n')) == 1 and content.startswith('.') and len(content) < 10:
        return True
    
    # 単一のファイルパス（拡張子を含む短いパス）
    if len(content.split('\n')) == 1 and ('.' in content) and len(content) < 50:
        # Windowsパス、Unixパスの形式チェック
        if ('\\' in content or '/' in content) and content.count('.') == 1:
            return True
    
    # 単語が1つだけで、明らかにコードではない
    words = content.split()
    if len(words) == 1 and len(words[0]) < 20:
        # 一般的なファイル名パターン
        if '.' in words[0] and not any(char in words[0] for char in '()[]{}=+-*/<>'):
            return True
    
    return False

def is_likely_code_content(code_content):
    """
    コンテンツが実際のコードである可能性が高いかを判定する
    
    Args:
        code_content (str): コードブロックの内容
        
    Returns:
        bool: コードである可能性が高い場合はTrue
    """
    if not code_content or not code_content.strip():
        return False
    
    content = code_content.strip()
    
    # 複数行の場合はコードの可能性が高い
    if len(content.split('\n')) > 1:
        return True
    
    # プログラミング言語のキーワードや記号が含まれている
    code_indicators = [
        '()', '[]', '{}', '=', '+=', '-=', '*=', '/=',
        'function', 'def ', 'class ', 'import ', 'from ',
        'var ', 'let ', 'const ', 'if ', 'else', 'for ',
        'while ', 'return', 'print', 'console.log',
        '#!/', '<?', '?>', '<script', '</script>',
        'SELECT', 'FROM', 'WHERE', 'INSERT', 'UPDATE'
    ]
    
    for indicator in code_indicators:
        if indicator in content:
            return True
    
    # 長いテキスト（50文字以上）でスペースが少ない場合
    if len(content) > 50 and content.count(' ') / len(content) < 0.1:
        return True
    
    return False

def convert_code_blocks(markdown_text, debug_html_path=None):
    """
    Markdownのコードブロックを適切な形式に変換する
    言語指定のないコードブロックにbashを追加する
    
    Args:
        markdown_text (str): 変換するMarkdownテキスト
        debug_html_path (str, optional): デバッグ用HTMLを保存するパス
        
    Returns:
        str: 変換後のテキスト
    """
    import re
    import markdown
    from bs4 import BeautifulSoup
    from loguru import logger
    logger.info("convert_code_blocks 関数を開始します")
    logger.debug(f"入力されたマークダウンの長さ: {len(markdown_text)} 文字")
    
    # マークダウン内のコードブロック数をカウント（簡易的な方法）
    md_code_blocks_count = markdown_text.count("```")
    logger.debug(f"マークダウン内のコードブロック区切り文字 (```) の数: {md_code_blocks_count}")
    
    # Step 1: マークダウンをHTMLに変換
    logger.info("マークダウンをHTMLに変換します")
    html = markdown.markdown(markdown_text, extensions=['fenced_code', 'tables', 'nl2br'])
    
    # デバッグ用: HTMLを保存
    if debug_html_path:
        with open(debug_html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        logger.info(f"HTMLをファイル {debug_html_path} に保存しました")
    
    # Step 2: BeautifulSoupでHTMLを解析
    logger.info("HTMLをBeautifulSoupで解析します")
    soup = BeautifulSoup(html, 'html.parser')
    
    # Step 3: コードブロックを見つける
    code_blocks = soup.find_all('code')
    logger.info(f"HTML内のcodeタグの総数: {len(code_blocks)}")
    
    # 言語指定のあるブロックと言語指定のないブロックをカウント
    lang_blocks = []
    no_lang_blocks = []
    
    for code in code_blocks:
        if code.get('class'):
            lang_blocks.append(code)
            logger.debug(f"言語指定あり: {code.get('class')} - 内容の一部: {code.text[:20]}...")
        else:
            no_lang_blocks.append(code)
            logger.debug(f"言語指定なし - 内容の一部: {code.text[:20]}...")
    
    logger.info(f"言語指定のあるコードブロック: {len(lang_blocks)}個")
    logger.info(f"言語指定のないコードブロック: {len(no_lang_blocks)}個")
    
    # Step 4: 言語指定のないコードブロックをマークダウンで探して置換
    replacements_made = 0
    result_text = markdown_text
    
    for code_block in no_lang_blocks:
        code_content = code_block.text.strip()
        logger.debug(f"変換対象のコードブロック: {code_content[:30]}...")
        
        # 以下の条件に該当する場合はスキップ（コードブロックではない可能性が高い）
        if should_skip_code_block(code_content):
            logger.debug(f"コードブロックではないと判断してスキップ: {code_content[:20]}...")
            continue
        
        match_found = False
        
        try:
            # エスケープして正規表現で安全に使用
            escaped_content = re.escape(code_content)
            
            # パターン1: 完全一致を試す（空白の扱いを柔軟に）
            patterns_to_try = [
                # 厳密な完全一致
                r'```\s*\n' + escaped_content + r'\s*\n```',
                # 前後の空白を柔軟に処理
                r'```\s*' + escaped_content + r'\s*```',
                # 改行の扱いを柔軟に
                r'```\s*\n?' + escaped_content + r'\n?\s*```'
            ]
            
            for i, pattern in enumerate(patterns_to_try):
                old_text = result_text
                result_text = re.sub(pattern, f'```bash\n{code_content}\n```', result_text, flags=re.MULTILINE | re.DOTALL)
                
                if old_text != result_text:
                    replacements_made += 1
                    match_found = True
                    logger.debug(f"パターン{i+1}で置換されました（{replacements_made}件目）")
                    break
            
            # 完全一致しなかった場合、コードの先頭部分だけで検索
            if not match_found and len(code_content) > 10:
                lines = code_content.split('\n')
                if lines:
                    first_line = re.escape(lines[0].strip())
                    if first_line:  # 空行でない場合のみ
                        prefix_patterns = [
                            r'```\s*\n' + first_line + r'[\s\S]*?\n```',
                            r'```\s*' + first_line + r'[\s\S]*?```'
                        ]
                        
                        for pattern in prefix_patterns:
                            old_text = result_text
                            result_text = re.sub(pattern, f'```bash\n{code_content}\n```', result_text, flags=re.MULTILINE | re.DOTALL)
                            
                            if old_text != result_text:
                                replacements_made += 1
                                match_found = True
                                logger.debug(f"先頭一致パターンで置換されました（{replacements_made}件目）")
                                break
                            
                        if match_found:
                            break
        
        except re.error as e:
            logger.warning(f"正規表現エラー: {e}, コンテンツ: {code_content[:30]}...")
            continue
        
        if not match_found:
            # 実際のコードっぽい内容の場合のみ警告
            if is_likely_code_content(code_content):
                logger.warning(f"コードブロック「{code_content[:30]}...」の対応するマークダウンが見つかりませんでした")
            else:
                logger.debug(f"テキストコンテンツ「{code_content[:30]}...」はコードブロックとして処理不要")
    
    logger.info(f"合計 {replacements_made}件 のコードブロックをbash指定に変換しました")
    
    # Step 5: 結果を確認するためにもう一度HTMLに変換（デバッグ用）
    if debug_html_path:
        check_html = markdown.markdown(result_text, extensions=['fenced_code', 'tables', 'nl2br'])
        check_soup = BeautifulSoup(check_html, 'html.parser')
        
        remaining_no_lang = sum(1 for code in check_soup.find_all('code') if not code.get('class'))
        logger.info(f"変換後の言語指定のないコードブロック: {remaining_no_lang}個")
        
        if remaining_no_lang > 0:
            logger.warning("一部のコードブロックは変換されませんでした")
    
    return result_text


def convert_mermaid_blocks(markdown_text):
    """
    MermaidブロックをWordPress用に変換する
    
    Args:
        markdown_text (str): 変換するMarkdownテキスト
        
    Returns:
        str: 変換後のテキスト
    """
    # Mermaidブロックを検出して置換する正規表現パターン
    pattern = r'```mermaid\n(.*?)\n```'
    
    def replace_mermaid(match):
        mermaid_content = match.group(1)
        return (
            '<!-- wp:wp-mermaid/block -->\n'
            '<div class="wp-block-wp-mermaid-block mermaid">\n'
            f'{mermaid_content}\n'
            '</div>\n'
            '<!-- /wp:wp-mermaid/block -->'
        )
    
    # Mermaidブロックを置換
    processed_text = re.sub(pattern, replace_mermaid, markdown_text, flags=re.DOTALL)
    return processed_text

def convert_markdown_with_mermaid(markdown_text):
    """
    Markdownテキストを変換する
    - 言語指定のないコードブロックをbashとして変換
    - MermaidブロックをWordPress用に変換
    
    Args:
        markdown_text (str): 変換するMarkdownテキスト
        
    Returns:
        str: 変換後のテキスト
    """
    processed_text = convert_code_blocks(markdown_text)
    processed_text = convert_mermaid_blocks(processed_text)
    return processed_text

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    # .envファイルから環境変数を読み込む
    load_dotenv()

    # 環境変数から設定を読み込む
    BASE_URL = os.getenv('BASE_URL')
    AUTH_USER = os.getenv('AUTH_USER')
    AUTH_PASS = os.getenv('AUTH_PASS')

    # WordPressAPIのインスタンスを作成
    wp_api = WordPressAPI(BASE_URL, AUTH_USER, AUTH_PASS)

    with open(r"draft\14_poke\pokedex-article.md", 'r', encoding='utf-8') as file:
        content = file.read()

    # カテゴリとタグの取得をテスト
    categories, tags = wp_api.get_existing_categories_and_tags()
    # print(f"取得したカテゴリ: {categories}")
    # print(f"取得したタグ: {tags}")
    

    # テスト投稿の作成
    class TestPost:
        def __init__(self):
            self.title = "テスト投稿"
            self.content = content
            self.slug = "test-post"
            self.categories = [{"name": "テストカテゴリ", "slug": "test-category"}]
            self.tags = [{"name": "テストタグ", "slug": "test-tag"}]

    test_post = TestPost()
    post_id = wp_api.create_post(test_post)
    print(f"作成された投稿のID: {post_id}")

    # テスト画像のアップロード（実際の画像ファイルパスに置き換えてください）
    # wp_api.upload_thumbnail(post_id, "path/to/test/image.jpg")

