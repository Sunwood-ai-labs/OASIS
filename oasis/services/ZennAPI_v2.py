import os
import random
import re
from typing import List, Optional
from loguru import logger
from art import *

class ZennAPIV2:
    def __init__(self):
        logger.info("ZennAPIV2 インスタンスを初期化しています...")
        self.emojis = [
            "😊", "🚀", "🌟", "🔥", "💡", "🎉", "👍", "🌈", "🍀", "🎨",
            "🐱", "🐶", "🦄", "🍎", "🍕", "🎸", "📚", "⚡", "🔍", "🏆"
        ]

    def get_random_emoji(self) -> str:
        return random.choice(self.emojis)

    def convert_twitter_embeds(self, content: str) -> str:
        def replace_blockquote(match):
            blockquote = match.group(0)
            url_pattern = r'https://twitter\.com/\w+/status/\d+'
            urls = re.findall(url_pattern, blockquote)
            if urls:
                return f'@[tweet]({urls[0]})\n\n'
            return ''

        # <blockquote>タグを置換
        pattern = r'<blockquote class="twitter-tweet"[^>]*>.*?</blockquote>'
        converted_content = re.sub(pattern, replace_blockquote, content, flags=re.DOTALL | re.IGNORECASE)

        return converted_content

    def create_article(self, 
                       title: str,
                       slug: str,
                       content_md: str,
                       emoji: Optional[str] = None,
                       type: str = "tech",
                       topics: List[str] = ["Python", "Selenium", "自動化"],
                       image_file: Optional[str] = None,
                       output_dir: str = "articles"):
        tprint('>>  ZennAPI V2')
        logger.info("記事の作成を開始します...")

        if emoji is None:
            emoji = self.get_random_emoji()
            logger.info(f"ランダムな絵文字を選択しました: {emoji}")
        
        # Twitter の埋め込みコードを変換
        converted_content = self.convert_twitter_embeds(content_md)
        logger.info("Twitter の埋め込みコードを変換しました")

        # 指定されたフォーマットで内容を作成
        content = f"""---
title: "{title}"
emoji: "{emoji}"
type: "{type}"
topics: {str(topics)}
published: false
---

{converted_content.strip()}
"""

        # 出力ディレクトリが存在しない場合は作成
        logger.debug(f"output_dir: {output_dir}")
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"出力ディレクトリを確認/作成しました: {output_dir}")

        # slugをファイル名として使用してファイルを作成
        file_path = os.path.join(output_dir, f"{slug[:48]}.md")
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        logger.success(f"記事ファイルを作成しました: {file_path}")
        
        # 変換後の内容をログに出力（確認用）
        # logger.info("変換後の内容:")
        # logger.info(content)

if __name__ == "__main__":
    zenn_api = ZennAPIV2()
    
    sample_content = """
# こんにちは、Zenn！

これは自動生成された記事のサンプル内容です。

## セクション1

ここにコンテンツが入ります。

## セクション2

さらにコンテンツが続きます。

<blockquote class="twitter-tweet" data-media-max-width="560"><p lang="ja" dir="ltr">mamba-codestral-7B-v0.1がGoogleColab L4で動いた！！ <a href="https://t.co/LKxQo1a8aQ">https://t.co/LKxQo1a8aQ</a> <a href="https://t.co/gI1mFPpCaQ">pic.twitter.com/gI1mFPpCaQ</a></p>&mdash; Maki@Sunwood AI Labs. (@hAru_mAki_ch) <a href="https://twitter.com/hAru_mAki_ch/status/1813589164736360670?ref_src=twsrc%5Etfw">July 17, 2024</a></blockquote> 

<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
"""
    
    zenn_api.create_article(
        title="Seleniumを使用したZenn記事の自動投稿",
        slug="selenium-zenn-auto-post",
        content_md=sample_content,
        type="tech",
        topics=["Python", "Selenium", "自動化", "Zenn"],
        output_dir=r"C:\Prj\Zenn\articles"
    )
