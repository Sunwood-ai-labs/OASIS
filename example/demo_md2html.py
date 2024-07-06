import mistune
import re

def preserve_blockquotes(md_text):
    # blockquoteを一時的に置換
    blockquotes = re.findall(r'<blockquote.*?>.*?</blockquote>', md_text, re.DOTALL)
    for i, block in enumerate(blockquotes):
        md_text = md_text.replace(block, f'BLOCKQUOTE_PLACEHOLDER_{i}')
    return md_text, blockquotes

def restore_blockquotes(html_body, blockquotes):
    # blockquoteを元に戻す
    for i, block in enumerate(blockquotes):
        html_body = html_body.replace(f'BLOCKQUOTE_PLACEHOLDER_{i}', block)
    return html_body

def make_inline_code_bold(html_body):
    # <pre>タグ内のコードブロックを一時的に置換
    code_blocks = re.findall(r'<pre><code.*?>.*?</code></pre>', html_body, re.DOTALL)
    for i, block in enumerate(code_blocks):
        html_body = html_body.replace(block, f'CODE_BLOCK_PLACEHOLDER_{i}')

    # インラインコードを太字に変換
    html_body = re.sub(r'<code>(.*?)</code>', r'<strong>\1</strong>', html_body)

    # コードブロックを元に戻す
    for i, block in enumerate(code_blocks):
        html_body = html_body.replace(f'CODE_BLOCK_PLACEHOLDER_{i}', block)

    return html_body

# マークダウンテキスト
md_text = """
# タイトル

- 項目1
  - サブ項目1.1
  - サブ項目1.2
- 項目2
  - サブ項目2.1
    - サブサブ項目2.1.1
  - サブ項目2.2

```python
def hello_world():
    print("Hello, World!")
```

`hello` and `def`

```python
def hello_world():
    print("Hello, World!")
```

<blockquote class="twitter-tweet"><p lang="ja" dir="ltr">HTMLで構造化されているのでインラインコードの変換も秒で終わってしまった。。。 <a href="https://t.co/PnEYG7IgWx">https://t.co/PnEYG7IgWx</a> <a href="https://t.co/nL45cMVMtL">pic.twitter.com/nL45cMVMtL</a></p>&mdash; Maki@Sunwood AI Labs. (@hAru_mAki_ch) <a href="https://twitter.com/hAru_mAki_ch/status/1809595150987063443?ref_src=twsrc%5Etfw">July 6, 2024</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
"""

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

# HTMLをファイルに保存
output_file = "output_mistune.html"

with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_body)

print(f"HTMLが {output_file} に保存されました。")
