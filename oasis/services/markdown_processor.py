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
        content, script_tags = self._preserve_script_tags(content)
        content, blockquotes = self._preserve_blockquotes(content)
        html_body = self._convert_to_html(content)
        if DEBUG : save_html_file(html_body, "_html_body_convert_to_html.html")
        html_body = self._make_inline_code_bold(html_body)
        if DEBUG : save_html_file(html_body, "_html_body_make_inline_code_bold.html")
        html_body = self._restore_blockquotes(html_body, blockquotes)
        if DEBUG : save_html_file(html_body, "_html_body_restore_blockquotes.html")
        html_body = self._restore_script_tags(html_body, script_tags)
        if DEBUG : save_html_file(html_body, "_html_body_restore_script_tags.html")
        return html_body

    def _preserve_script_tags(self, content):
        script_tags = re.findall(r'<script.*?>.*?</script>', content, re.DOTALL)
        for i, tag in enumerate(script_tags):
            content = content.replace(tag, f'SCRIPT_TAG_PLACEHOLDER_{i}')
        return content, script_tags

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
        html_body = re.sub(r'<code>([^<\n]+)</code>', r'<strong>\1</strong>', html_body)
        return html_body

    def _restore_script_tags(self, html_body, script_tags):
        for i, tag in enumerate(script_tags):
            html_body = html_body.replace(f'SCRIPT_TAG_PLACEHOLDER_{i}', tag)
        return html_body

def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def save_html_file(html_content, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTMLが {file_path} に保存されました。")

if __name__ == "__main__":
    input_file = r"draft\roomba01\README.md"  # 入力するマークダウンファイルの名前
    output_file = "output_mistune.html"  # 出力するHTMLファイルの名前

    markdown_content = read_markdown_file(input_file)
    processor = MarkdownProcessor()
    html_content = processor.convert_markdown_to_html(markdown_content)
    save_html_file(html_content, output_file)
