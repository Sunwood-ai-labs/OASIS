
import mistune
import re

try:
    from .link_preview_generator import generate_site_card, generate_iframely_embed
except:
    from link_preview_generator import generate_site_card, generate_iframely_embed

DEBUG = False

class MarkdownProcessor:
    def __init__(self):
        self.markdown = mistune.create_markdown(
            renderer=mistune.HTMLRenderer(),
            plugins=['table', 'url', 'strikethrough', 'footnotes', 'task_lists']
        )

    def convert_markdown_to_html(self, content: str) -> str:
        content, link_previews = self._process_link_previews(content)
        content, blockquotes = self._preserve_blockquotes(content)
        html_body = self._convert_to_html(content)
        if DEBUG : save_html_file(html_body, "_html_body_convert_to_html.html")
        html_body = self._make_inline_code_bold(html_body)
        if DEBUG : save_html_file(html_body, "_html_body_make_inline_code_bold.html")
        html_body = self._restore_blockquotes(html_body, blockquotes)
        if DEBUG : save_html_file(html_body, "_html_body_restore_blockquotes.html")
        html_body = self._restore_link_previews(html_body, link_previews)
        if DEBUG : save_html_file(html_body, "_html_body_restore_link_previews.html")
        return html_body

    def _process_link_previews(self, content):
        link_previews = {}
        def replace_url_with_placeholder(match):
            url = match.group(0)

            # simple card
            # preview_html = generate_site_card(url)

            # iframe
            preview_html = generate_iframely_embed(url)


            placeholder = f"LINK_PREVIEW_PLACEHOLDER_{len(link_previews)}"
            link_previews[placeholder] = preview_html
            return f"{url}\n\n{placeholder}\n"

        processed_text = re.sub(r'^https?://\S+$', replace_url_with_placeholder, content, flags=re.MULTILINE)
        return processed_text, link_previews

    def _preserve_blockquotes(self, content):
        blockquotes = re.findall(r'<blockquote.*?>.*?</blockquote>', content, re.DOTALL)
        for i, block in enumerate(blockquotes):
            content = content.replace(block, f'BLOCKQUOTE_PLACEHOLDER_{i}')
        return content, blockquotes

    def _convert_to_html(self, content):
        return self.markdown(content)

    def _restore_blockquotes(self, html_body, blockquotes):
        for i, block in enumerate(blockquotes):
            html_body = html_body.replace(f'BLOCKQUOTE_PLACEHOLDER_{i}', block)
        return html_body

    def _make_inline_code_bold(self, html_body):
        # code_blocks = re.findall(r'<pre><code.*?>.*?</code></pre>', html_body, re.DOTALL)
        # for i, block in enumerate(code_blocks):
        #     html_body = html_body.replace(block, f'CODE_BLOCK_PLACEHOLDER_{i}')

        # html_body = re.sub(r'<code>(.*?)</code>', r'<strong>\1</strong>', html_body)
        html_body = re.sub(r'<code>([^<\n]+)</code>', r'<strong>\1</strong>', html_body)
        # for i, block in enumerate(code_blocks):
        #     html_body = html_body.replace(f'CODE_BLOCK_PLACEHOLDER_{i}', block)

        return html_body

    def _restore_link_previews(self, html_body, link_previews):
        for placeholder, preview_html in link_previews.items():
            html_body = html_body.replace(placeholder, preview_html)
        return html_body

def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def save_html_file(html_content, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTMLが {file_path} に保存されました。")

if __name__ == "__main__":

    input_file = r"draft\ARC01\ARC01.md"  # 入力するマークダウンファイルの名前
    output_file = "output_mistune.html"  # 出力するHTMLファイルの名前

    markdown_content = read_markdown_file(input_file)
    processor = MarkdownProcessor()
    html_content = processor.convert_markdown_to_html(markdown_content)
    save_html_file(html_content, output_file)

