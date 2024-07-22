import argparse
import os
import sys
import subprocess
import random
from loguru import logger

# loguruの設定
logger.remove()  # デフォルトのハンドラを削除
logger.add(sys.stderr, level="DEBUG")  # 標準エラー出力にDEBUGレベルで出力
logger.add("process.log", rotation="500 MB", level="DEBUG")

def is_supported_format(file_path):
    """サポートされているファイル形式かチェックする"""
    supported_extensions = ['.rst', '.md', '.markdown']
    _, ext = os.path.splitext(file_path)
    return ext.lower() in supported_extensions

def convert_markdown_to_rst(input_file):
    """マークダウンファイルをreStructuredTextに変換する"""
    output_file = os.path.splitext(input_file)[0] + '.rst'
    try:
        subprocess.run(['pandoc', '-f', 'markdown', '-t', 'rst', '-o', output_file, input_file], check=True)
        logger.info(f"マークダウンファイルをreStructuredTextに変換しました: {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        logger.error(f"マークダウンの変換に失敗しました: {str(e)}")
        return None

def add_transitions_to_rst(input_file):
    """rstファイルにダイナミックなトランジションを追加する"""
    transitions = [
        "fade", "slide", "convex", "concave", "zoom"
    ]
    
    with open(input_file, 'r', encoding="utf8") as file:
        content = file.readlines()
    
    new_content = []
    for line in content:
        if line.strip() == "----":  # スライドの区切り
            transition = random.choice(transitions)
            new_content.append(f":data-transition: {transition}\n")
        new_content.append(line)
    
    output_file = os.path.splitext(input_file)[0] + '_with_transitions.rst'
    with open(output_file, 'w', encoding="utf8") as file:
        file.writelines(new_content)
    
    logger.info(f"トランジションを追加したrstファイルを作成しました: {output_file}")
    return output_file

def generate_slides(input_file, output_dir, css_file=None):
    logger.info(f"スライド生成を開始します。入力: {input_file}, 出力ディレクトリ: {output_dir}")

    if not is_supported_format(input_file):
        logger.error(f"サポートされていないファイル形式です: {input_file}")
        return False

    # マークダウンファイルの場合、reStructuredTextに変換
    if input_file.lower().endswith(('.md', '.markdown')):
        rst_file = convert_markdown_to_rst(input_file)
        if not rst_file:
            return False
        input_file = rst_file

    # rstファイルにトランジションを追加
    # input_file_with_transitions = add_transitions_to_rst(input_file)
    input_file_with_transitions = input_file

    try:
        # Hovercraftのコマンドを構築
        command = ['hovercraft']
        if css_file:
            command.extend(['-c', css_file])
        command.extend([input_file_with_transitions, output_dir])

        # Hovercraftの実行
        subprocess.run(command, check=True)

        index_file = os.path.join(output_dir, 'index.html')
        if os.path.exists(index_file):
            logger.success(f"HTMLスライドの生成が完了しました: {index_file}")
            logger.debug(f"生成されたファイルのサイズ: {os.path.getsize(index_file)} bytes")
            return True
        else:
            logger.error(f"HTMLファイルが生成されませんでした: {index_file}")
            return False

    except subprocess.CalledProcessError as e:
        logger.error(f"Hovercraftの実行中にエラーが発生しました: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"スライド生成中にエラーが発生しました: {str(e)}")
        logger.exception("詳細なエラー情報:")
        return False

def main():
    parser = argparse.ArgumentParser(description="マークダウンまたはreStructuredTextをHTMLスライドに変換します")
    parser.add_argument("--input_file", default="presentation.rst", help="入力のマークダウンまたはreStructuredTextファイルのパス")
    parser.add_argument("-d", "--destination", default="output",
                        help="出力するHTMLファイルのディレクトリ (デフォルト: output)")
    parser.add_argument("-c", "--css", default="css/mytheme.css",help="カスタムCSSファイルのパス")
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        logger.error(f"入力ファイルが見つかりません: {args.input_file}")
        return

    success = generate_slides(args.input_file, args.destination, args.css)
    if success:
        logger.info(f"スライドの生成が完了しました。出力ディレクトリ: {args.destination}")
    else:
        logger.error("スライドの生成に失敗しました。")

if __name__ == "__main__":
    main()
