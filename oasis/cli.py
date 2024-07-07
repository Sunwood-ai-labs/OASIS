import argparse
import sys
from .oasis import OASIS
from .config import Config
from .logger import logger
from art import *

def main():
    tprint(">>  OASIS  <<", font="rnd-xlarge")
    parser = argparse.ArgumentParser(
        description="指定されたフォルダを処理し、WordPress, Qiita, Noteへの投稿を作成します。"
    )

    # main
    parser.add_argument('folder_path', type=str, help='処理するフォルダのパス')

    # llm
    parser.add_argument('--llm-model', type=str, help='使用するLLMモデル')
    parser.add_argument(
        '--max-retries', type=int, default=3, help='LLMリクエストの最大リトライ回数'
    )
    
    # mode
    parser.add_argument('--qiita', action='store_true', help='Qiitaにも投稿する')
    parser.add_argument('--note', action='store_true', help='Noteにも投稿する')
    parser.add_argument('--wp', action='store_true', help='WordPressにも投稿する')

    # wp
    parser.add_argument('--wp-user', type=str, help='WordPressのユーザー名')
    parser.add_argument('--wp-pass', type=str, help='WordPressのパスワード')
    parser.add_argument('--wp-url', type=str, help='WordPressのURL')

    # qiita
    parser.add_argument('--qiita-token', type=str, help='QiitaのAPIトークン')
    parser.add_argument('--qiita-post-publish', action='store_true', help='Qiitaの公開設定')

    # note
    parser.add_argument('--note-email', type=str, help='Noteのメールアドレス')
    parser.add_argument('--note-password', type=str, help='Noteのパスワード')
    parser.add_argument('--note-user-id', type=str, help='NoteのユーザーID')
    parser.add_argument('--note-publish', action='store_true', help='公開するかどうか')
    parser.add_argument('--note-api-ver', type=str, default="v2", help='NoteのAPI Ver')
    

    # Firefox 設定
    parser.add_argument('--firefox-binary-path', type=str, help='Firefox の実行ファイルへのパス')
    parser.add_argument('--firefox-profile-path', type=str, help='使用する Firefox プロファイルへのパス')
    parser.add_argument('--firefox-headless', action='store_true', help='Firefoxのヘッドレスモード')

    args = parser.parse_args()

    oasis = OASIS(
        base_url=args.wp_url or Config.BASE_URL,
        auth_user=args.wp_user or Config.AUTH_USER,
        auth_pass=args.wp_pass or Config.AUTH_PASS,
        llm_model=args.llm_model,
        max_retries=args.max_retries,
        qiita_token=args.qiita_token or Config.QIITA_TOKEN,
        qiita_post_private=not args.qiita_post_publish,
        note_email=args.note_email or Config.NOTE_EMAIL,
        note_password=args.note_password or Config.NOTE_PASSWORD,
        note_user_id=args.note_user_id or Config.NOTE_USER_ID,
        note_publish=args.note_publish,
        note_api_ver=args.note_api_ver,
        firefox_binary_path=args.firefox_binary_path,  # Firefox のパス
        firefox_profile_path=args.firefox_profile_path,  # Firefox のプロファイルパス
        firefox_headless=args.firefox_headless
    )
    logger.info(
        f"使用中のLLMモデル: {oasis.config.LLM_MODEL}, 最大リトライ回数: {args.max_retries}"
    )

    result = oasis.process_folder(
        args.folder_path, post_to_qiita=args.qiita, post_to_note=args.note, post_to_wp=args.wp
    )

    logger.info("投稿が正常に作成されました！")
    logger.info(f"タイトル: {result['title']}")
    logger.info("-" * 80)
    logger.info(f"スラグ: {result['slug']}")
    logger.info(f">>> categories :")
    for category in result['categories']:
        logger.info(f"- {category['name']} (ID: {category['slug']})")
    logger.info(">>> tags :")
    for tag in result['tags']:
        logger.info(f"- {tag['name']} (ID: {tag['slug']})")



if __name__ == '__main__':
    main()
