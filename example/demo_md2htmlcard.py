import mistune
import re
import requests
from bs4 import BeautifulSoup

def preserve_blockquotes(md_text):
    blockquotes = re.findall(r'<blockquote.*?>.*?</blockquote>', md_text, re.DOTALL)
    for i, block in enumerate(blockquotes):
        md_text = md_text.replace(block, f'BLOCKQUOTE_PLACEHOLDER_{i}')
    return md_text, blockquotes

def restore_blockquotes(html_body, blockquotes):
    for i, block in enumerate(blockquotes):
        html_body = html_body.replace(f'BLOCKQUOTE_PLACEHOLDER_{i}', block)
    return html_body

def make_inline_code_bold(html_body):
    code_blocks = re.findall(r'<pre><code.*?>.*?</code></pre>', html_body, re.DOTALL)
    for i, block in enumerate(code_blocks):
        html_body = html_body.replace(block, f'CODE_BLOCK_PLACEHOLDER_{i}')

    html_body = re.sub(r'<code>(.*?)</code>', r'<strong>\1</strong>', html_body)

    for i, block in enumerate(code_blocks):
        html_body = html_body.replace(f'CODE_BLOCK_PLACEHOLDER_{i}', block)

    return html_body

def get_site_metadata(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.title.string if soup.title else ''
        description = soup.find('meta', attrs={'name': 'description'})
        description = description['content'] if description else ''
        
        og_image = soup.find('meta', property='og:image')
        image_url = og_image['content'] if og_image else ''
        
        return {
            'title': title,
            'description': description,
            'image_url': image_url,
            'url': url
        }
    except:
        return {
            'title': url,
            'description': '',
            'image_url': '',
            'url': url
        }

def create_card_html(metadata):
    html = f"""
    <a href="{metadata['url']}" style="text-decoration: none; color: inherit;">
        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 16px; max-width: 400px; font-family: Arial, sans-serif; cursor: pointer; transition: box-shadow 0.3s;">
            <h2 style="margin-top: 0;">{metadata['title']}</h2>
            <p>{metadata['description']}</p>
            {f'<img src="{metadata["image_url"]}" style="max-width: 100%; height: auto;">' if metadata['image_url'] else ''}
            <p style="color: #0066cc; margin-bottom: 0;">{metadata['url']}</p>
        </div>
    </a>
    <style>
        a:hover > div {{
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
    </style>
    """
    return html

def generate_site_card(url):
    metadata = get_site_metadata(url)
    return create_card_html(metadata)

def process_link_previews(md_text):
    link_previews = {}
    def replace_url_with_placeholder(match):
        url = match.group(0)
        preview_html = generate_site_card(url)
        placeholder = f"LINK_PREVIEW_PLACEHOLDER_{len(link_previews)}"
        link_previews[placeholder] = preview_html
        return f"{url}\n\n{placeholder}\n"

    processed_text = re.sub(r'^https?://\S+$', replace_url_with_placeholder, md_text, flags=re.MULTILINE)
    return processed_text, link_previews

def convert_markdown_to_html(input_file, output_file):
    # マークダウンファイルを読み込む
    with open(input_file, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # リンクプレビューを処理
    md_text, link_previews = process_link_previews(md_text)

    # blockquoteを保存
    md_text, blockquotes = preserve_blockquotes(md_text)

    # Mistuneインスタンスを作成
    markdown = mistune.create_markdown(
        renderer=mistune.HTMLRenderer(),
        plugins=['table', 'url', 'strikethrough', 'footnotes', 'task_lists']
    )

    # マークダウンをHTMLに変換
    html_body = markdown(md_text)

    # blockquoteを復元
    html_body = restore_blockquotes(html_body, blockquotes)

    # インラインコードを太字に変換
    html_body = make_inline_code_bold(html_body)

    # リンクプレビューを復元
    for placeholder, preview_html in link_previews.items():
        html_body = html_body.replace(placeholder, preview_html)

    # HTMLをファイルに保存
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_body)

    print(f"HTMLが {output_file} に保存されました。")

# 使用例
input_file = r"draft\ARC01\ARC01.md"  # 入力するマークダウンファイルの名前
output_file = "output_mistune.html"  # 出力するHTMLファイルの名前

convert_markdown_to_html(input_file, output_file)
