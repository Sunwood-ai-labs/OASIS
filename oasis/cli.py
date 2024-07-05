import argparse
import sys
from .oasis import OASIS
from .config import Config
from .logger import logger
from art import *

def main():
    tprint(">>  OASIS  <<",font="rnd-large")
    parser = argparse.ArgumentParser(description="指定されたフォルダを処理し、WordPressとQiitaの投稿を作成します。")
    parser.add_argument('folder_path', type=str, help='処理するフォルダのパス')
    parser.add_argument('--llm-model', type=str, help='使用するLLMモデル')
    parser.add_argument('--max-retries', type=int, default=3, help='LLMリクエストの最大リトライ回数')
    parser.add_argument('--qiita', action='store_true', help='Qiitaにも投稿する')
    parser.add_argument('--wp-user', type=str, help='WordPressのユーザー名')
    parser.add_argument('--wp-pass', type=str, help='WordPressのパスワード')
    parser.add_argument('--wp-url', type=str, help='WordPressのURL')
    parser.add_argument('--qiita-token', type=str, help='QiitaのAPIトークン')
    
    args = parser.parse_args()

    try:
        oasis = OASIS(
            base_url=args.wp_url or Config.BASE_URL,
            auth_user=args.wp_user or Config.AUTH_USER,
            auth_pass=args.wp_pass or Config.AUTH_PASS,
            llm_model=args.llm_model,
            max_retries=args.max_retries,
            qiita_token=args.qiita_token or Config.QIITA_TOKEN
        )
        logger.info(f"使用中のLLMモデル: {oasis.config.LLM_MODEL}, 最大リトライ回数: {args.max_retries}")

        result = oasis.process_folder(args.folder_path, post_to_qiita=args.qiita)

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
