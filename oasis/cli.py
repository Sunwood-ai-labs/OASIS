import argparse
import sys
from .oasis import OASIS
from .config import Config
from .logger import logger
from art import *

def main():
    parser = argparse.ArgumentParser(description="指定されたフォルダを処理し、WordPressの投稿を作成します。")
    parser.add_argument('folder_path', type=str, help='処理するフォルダのパス')
    parser.add_argument('--llm-model', type=str, help='使用するLLMモデル')
    parser.add_argument('--max-retries', type=int, default=3, help='LLMリクエストの最大リトライ回数')
    
    args = parser.parse_args()
    tprint(">>  OASIS  <<",font="rnd-large")

    try:
        oasis = OASIS(llm_model=args.llm_model, max_retries=args.max_retries)
        logger.info(f"使用中のLLMモデル: {oasis.config.LLM_MODEL}, 最大リトライ回数: {args.max_retries}")

        result = oasis.process_folder(args.folder_path)

        logger.info("投稿が正常に作成されました！")
        logger.info(f"タイトル: {result['title']}")
        logger.info("-"*80)
        logger.info(f"スラグ: {result['slug']}")
        logger.info(f">>> categories :")
        for category in result['categories']:
            logger.info(f"- {category['name']} (ID: {category['slug']})")
        logger.info(">>> tags :")
        for tag in result['tags']:
            logger.info(f"- {tag['name']} (ID: {tag['slug']})")

    except Exception as e:
        logger.error(f"エラーが発生しました: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
