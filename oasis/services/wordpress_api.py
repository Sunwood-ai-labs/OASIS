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
        
        # wp 用に前処理
        mermaid_html = convert_markdown_to_html_with_mermaid(post.content)
        mermaid_md = convert_html_to_markdown_preserve_mermaid(mermaid_html)

        try:
            payload = {
                'title': post.title,
                'content': mermaid_md,
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



def convert_markdown_to_html_with_mermaid(markdown_text, output_dir='debug_output'):
    # 出力ディレクトリの作成
    os.makedirs(output_dir, exist_ok=True)

    # マークダウンをHTMLに変換（コードブロックのサポート付き）
    html = markdown.markdown(markdown_text, extensions=['fenced_code'])
    
    # 変換前のHTMLを保存
    with open(os.path.join(output_dir, 'before_conversion.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    
    # BeautifulSoupを使用してHTMLを解析
    soup = BeautifulSoup(html, 'html.parser')
    
    # BeautifulSoupのバージョンとパーサーを出力
    # print(f"Parser being used: {soup.parser}")

    # すべてのcodeタグを検索
    for code_block in soup.find_all('code'):
        # classが'language-mermaid'を含む場合のみ処理
        if code_block.has_attr('class') and 'language-mermaid' in code_block['class']:
            # 親のpreタグを新しい構造で置換
            new_block = soup.new_tag('div')
            new_block['class'] = 'wp-block-wp-mermaid-block mermaid'
            new_block.string = code_block.string
            
            wrapper = soup.new_tag('div')
            # Comment オブジェクトを直接作成
            wrapper.append(Comment(' wp:wp-mermaid/block '))
            wrapper.append(new_block)
            wrapper.append(Comment(' /wp:wp-mermaid/block '))
            
            code_block.parent.replace_with(wrapper)
    
    # 変換後のHTMLを保存
    converted_html = str(soup)
    with open(os.path.join(output_dir, 'after_conversion.html'), 'w', encoding='utf-8') as f:
        f.write(converted_html)

    return converted_html

def convert_html_to_markdown_preserve_mermaid(html_content):
    # Mermaidブロック、blockquote、Twitter埋め込み、コードブロックを一時的にプレースホルダーに置き換え
    special_blocks = []
    patterns = [
        r'(<!-- wp:wp-mermaid/block -->.*?<!-- /wp:wp-mermaid/block -->)',
        r'(<blockquote class="twitter-tweet".*?</blockquote>)',
        r'(<blockquote>.*?</blockquote>)',
        r'(<script async src="https://platform\.twitter\.com/widgets\.js" charset="utf-8"></script>)',
        r'(<pre><code.*?>.*?</code></pre>)'
    ]
    
    def replace_special_block(match):
        block = match.group(1)
        if block.startswith('<pre><code'):
            # コードブロックの処理
            soup = BeautifulSoup(block, 'html.parser')
            code_block = soup.find('code')
            
            # 言語情報を取得
            language = ''
            if code_block.has_attr('class'):
                classes = code_block['class']
                language_class = next((c for c in classes if c.startswith('language-')), None)
                if language_class:
                    language = language_class.split('-')[1]
            
            # コードの内容を取得し、HTMLエンティティをデコード
            code_content = html.unescape(code_block.string)
            
            # マークダウン形式のコードブロックを作成
            markdown_code = f"```{language}\n{code_content}\n```"
            special_blocks.append(markdown_code)
        else:
            special_blocks.append(block)
        return f'__SPECIAL_BLOCK_PLACEHOLDER_{len(special_blocks) - 1}__'


    with open("html_content.html", 'w', encoding='utf-8') as file:
        file.write(html_content)    
    html_with_placeholders = html_content

    for pattern in patterns:
        html_with_placeholders = re.sub(pattern, replace_special_block, html_with_placeholders, flags=re.DOTALL)
    
    with open("html_with_placeholders.html", 'w', encoding='utf-8') as file:
        file.write(html_with_placeholders)
        
    # HTMLをマークダウンに変換
    h = html2text.HTML2Text()
    h.body_width = 0  # 行の折り返しを無効化
    markdown_text = h.handle(html_with_placeholders)
    
    with open("markdown_text.md", 'w', encoding='utf-8') as file:
        file.write(markdown_text)
        
    # プレースホルダーを特殊ブロックに戻す
    for i, block in enumerate(special_blocks):
        print("----------------")
        print(i)
        print(block)
        markdown_text = markdown_text.replace(f'__SPECIAL_BLOCK_PLACEHOLDER_{i}__', block + "\n")
    
    markdown_text = markdown_text.replace("<!-- /wp:wp-mermaid/block --> ", "<!-- /wp:wp-mermaid/block -->")

    with open("markdown_text2.md", 'w', encoding='utf-8') as file:
        file.write(markdown_text)
    
    return markdown_text

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

    with open(r"article_draft\45_Kolors\README.md", 'r', encoding='utf-8') as file:
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

