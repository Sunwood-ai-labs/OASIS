import argparse
import os
from loguru import logger
from litellm import completion

# loguruの設定
logger.add("process.log", rotation="500 MB")

def read_file(file_path):
    logger.info(f"ファイル '{file_path}' を読み込んでいます")
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    logger.success(f"ファイルの読み込みが完了しました")
    return content

def convert_to_slides(markdown_text):
    logger.info("マークダウンをスライド形式に変換しています")
    prompt = f"""
以下のマークダウンをスライド形式のマークダウンに変換してください。
変換の際は、次のルールに従ってください：

1. タイトルは# (h1)で表現してください。
2. 章見出しは## (h2)のみを使用してください。
3. 箇条書きを駆使してスライドの内容を構成してください。
4. 各h2の見出しの間には必ず"---"を挿入してスライドを区切ってください。
5. コンテンツは簡潔に、1スライドあたり3-5項目程度にまとめてください。

変換するマークダウンの内容：

{markdown_text}
    """
    
    response = completion(
        model="gemini/gemini-1.5-pro-latest",
        messages=[{"role": "user", "content": prompt}]
    )
    slides_content = response.choices[0].message.content
    logger.success("スライド形式への変換が完了しました")
    return slides_content

def save_markdown_file(content, output_path):
    logger.info(f"マークダウンファイルを '{output_path}' に保存しています")
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(content)
    logger.success(f"マークダウンファイルの保存が完了しました: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="マークダウンをスライド形式に変換")
    parser.add_argument("--input_file", default="_presentation.md", help="入力マークダウンファイルのパス")
    parser.add_argument("--output_file", default="presentation.md", help="出力スライドマークダウンファイルのパス")
    args = parser.parse_args()

    markdown_content = read_file(args.input_file)
    slides_content = convert_to_slides(markdown_content)
    save_markdown_file(slides_content, args.output_file)

if __name__ == "__main__":
    main()
