import argparse
import os
import sys
import subprocess
import random
import re
from loguru import logger

# loguruの設定
logger.remove()  # デフォルトのハンドラを削除
logger.add(sys.stderr, level="DEBUG")  # 標準エラー出力にDEBUGレベルで出力
logger.add("process.log", rotation="500 MB", level="DEBUG")

# グリッドサイズの定義
GRID_WIDTH = 5000
GRID_HEIGHT = 3000
SLIDE_WIDTH = 1000
SLIDE_HEIGHT = 750

class BoundingBox:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def intersects(self, other):
        return not (self.x + self.width <= other.x or
                    other.x + other.width <= self.x or
                    self.y + self.height <= other.y or
                    other.y + other.height <= self.y)

def get_random_position(used_bounding_boxes):
    """ランダムな位置を生成し、既存のスライドと重ならないようにする"""
    max_attempts = 100
    for _ in range(max_attempts):
        x = random.randint(0, (GRID_WIDTH - SLIDE_WIDTH) // SLIDE_WIDTH) * SLIDE_WIDTH
        y = random.randint(0, (GRID_HEIGHT - SLIDE_HEIGHT) // SLIDE_HEIGHT) * SLIDE_HEIGHT
        new_box = BoundingBox(x, y, SLIDE_WIDTH, SLIDE_HEIGHT)
        
        if not any(new_box.intersects(box) for box in used_bounding_boxes):
            return x, y

    logger.warning("スライドの配置に失敗しました。ランダムな位置を返します。")
    return x, y

def convert_markdown_to_hovercraft_rst(input_file, output_file):
    """マークダウンファイルをHovercraft用のrstファイルに変換し、重ならない位置を設定する"""
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # マークダウンの見出しをrstの見出しに変換
    content = re.sub(r'^# (.+)$', r'\1\n' + '=' * 80, content, flags=re.MULTILINE)
    content = re.sub(r'^## (.+)$', r'\1\n' + '-' * 80, content, flags=re.MULTILINE)
    content = re.sub(r'^### (.+)$', r'\1\n' + '~' * 80, content, flags=re.MULTILINE)

    # リストアイテムの変換
    content = re.sub(r'^- (.+)$', r'* \1', content, flags=re.MULTILINE)

    # スライドを分割
    slides = re.split(r'\n---\n', content)

    new_content = [":title: Your Presentation Title",
                   ":data-transition-duration: 1000",
                   ":css: css/mytheme.css",
                   ""]  # ヘッダーを設定

    used_bounding_boxes = []

    for slide in slides:
        # 重ならない位置を取得
        x, y = get_random_position(used_bounding_boxes)
        used_bounding_boxes.append(BoundingBox(x, y, SLIDE_WIDTH, SLIDE_HEIGHT))
        
        # 新しいスライド内容を構築
        new_slide = f"----\n\n:data-x: {x}\n:data-y: {y}\n\n{slide.strip()}\n"
        new_content.append(new_slide)

    # 出力ファイルに書き込み
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(new_content))

    logger.info(f"Hovercraft用のrstファイルを作成しました: {output_file}")
    return output_file

# 以下の関数は変更なし
def is_supported_format(file_path):
    """サポートされているファイル形式かチェックする"""
    supported_extensions = ['.rst', '.md', '.markdown']
    _, ext = os.path.splitext(file_path)
    return ext.lower() in supported_extensions

def generate_slides(input_file, output_dir, css_file=None):
    logger.info(f"スライド生成を開始します。入力: {input_file}, 出力ディレクトリ: {output_dir}")

    if not is_supported_format(input_file):
        logger.error(f"サポートされていないファイル形式です: {input_file}")
        return False

    # マークダウンファイルの場合、Hovercraft用のrstに変換
    if input_file.lower().endswith(('.md', '.markdown')):
        rst_file = os.path.splitext(input_file)[0] + '_hovercraft.rst'
        rst_file = convert_markdown_to_hovercraft_rst(input_file, rst_file)
    elif input_file.lower().endswith('.rst'):
        rst_file = input_file
    else:
        logger.error(f"サポートされていないファイル形式です: {input_file}")
        return False

    try:
        # Hovercraftのコマンドを構築
        command = ['hovercraft']
        if css_file:
            command.extend(['-c', css_file])
        command.extend([rst_file, output_dir])

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
    parser.add_argument("--input_file", default="presentation.md", help="入力のマークダウンまたはreStructuredTextファイルのパス")
    parser.add_argument("-d", "--destination", default="output",
                        help="出力するHTMLファイルのディレクトリ (デフォルト: output)")
    parser.add_argument("-c", "--css", default="css/mytheme.css", help="カスタムCSSファイルのパス")
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
