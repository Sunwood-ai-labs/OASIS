import argparse
import os
import sys
from loguru import logger
from landslide.generator import Generator
from landslide.parser import Parser

# loguruの設定
logger.remove()  # デフォルトのハンドラを削除
logger.add(sys.stderr, level="DEBUG")  # 標準エラー出力にDEBUGレベルで出力
logger.add("process.log", rotation="500 MB", level="DEBUG")

def is_supported_format(file_path):
    """サポートされているファイル形式かチェックする"""
    supported_extensions = ['.md', '.markdown', '.rst', '.textile']
    _, ext = os.path.splitext(file_path)
    return ext.lower() in supported_extensions

def generate_slides(input_file, output_file, theme='default', embed=True):
    logger.info(f"スライド生成を開始します。入力: {input_file}, 出力: {output_file}")

    if not is_supported_format(input_file):
        logger.error(f"サポートされていないファイル形式です: {input_file}")
        return False

    try:
        # Generatorの設定
        gen = Generator(
            source=input_file,
            destination=output_file,
            theme=theme,
            embed=embed,
            encoding='utf8',
            logger=logger.info  # Landslideのログ出力にloguruを使用
        )

        # スライドの生成
        gen.execute()

        if os.path.exists(output_file):
            logger.success(f"HTMLスライドの生成が完了しました: {output_file}")
            logger.debug(f"生成されたファイルのサイズ: {os.path.getsize(output_file)} bytes")
            return True
        else:
            logger.error(f"HTMLファイルが生成されませんでした: {output_file}")
            return False

    except Exception as e:
        logger.error(f"スライド生成中にエラーが発生しました: {str(e)}")
        logger.exception("詳細なエラー情報:")
        return False

def main():
    parser = argparse.ArgumentParser(description="マークダウンをHTMLスライドに変換します")
    parser.add_argument("--input_file", default=r"article_draft\demo_land\README.md", help="入力のマークダウンファイルのパス")
    parser.add_argument("-d", "--destination", default="presentation.html",
                        help="出力するHTMLファイルのパス (デフォルト: presentation.html)")
    parser.add_argument("-t", "--theme", default="default",
                        help="使用するテーマ (デフォルト: default)")
    parser.add_argument("-e", "--embed", action="store_true",
                        help="リソースを埋め込む")
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        logger.error(f"入力ファイルが見つかりません: {args.input_file}")
        return

    success = generate_slides(args.input_file, args.destination, args.theme, args.embed)
    if success:
        logger.info(f"スライドの生成が完了しました。出力ファイル: {args.destination}")
    else:
        logger.error("スライドの生成に失敗しました。")

if __name__ == "__main__":
    main()
