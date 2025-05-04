import argparse
import sys
from .oasis import OASIS
from .config import Config
from .logger import logger
from art import *
import os

def main():
    tprint(">>  OASIS  <<", font="rnd-xlarge")
    parser = argparse.ArgumentParser(
        description="Markdown記事をWordPress, Qiita, Note, Zennに投稿します。フォルダを指定するか、マークダウンファイルと画像を直接指定できます。"
    )

    # ファイル/フォルダ指定
    file_group = parser.add_mutually_exclusive_group()
    file_group.add_argument('--folder', type=str, help='処理するフォルダのパス')
    file_group.add_argument('--markdown', type=str, help='投稿するマークダウンファイルのパス')
    parser.add_argument('--image', type=str, help='サムネイル画像のパス（マークダウンファイルと一緒に使用）')

    # llm
    parser.add_argument('--llm-model', type=str, help='使用するLLMモデル')
    parser.add_argument(
        '--max-retries', type=int, default=10, help='LLMリクエストの最大リトライ回数'
    )
    
    # mode
    parser.add_argument('--qiita', action='store_true', help='Qiitaにも投稿する')
    parser.add_argument('--note', action='store_true', help='Noteにも投稿する')
    parser.add_argument('--wp', action='store_true', help='WordPressにも投稿する')
    parser.add_argument('--zenn', action='store_true', help='Zennにも投稿する')

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
    
    # zenn
    # parser.add_argument('--qiita-token', type=str, help='QiitaのAPIトークン')
    # parser.add_argument('--qiita-post-publish', action='store_true', help='Qiitaの公開設定')
    parser.add_argument('--zenn-output-path', default=r"C:\Prj\Zenn\articles", help='ZennAPI V2の出力フォルダ')
    parser.add_argument('--zenn-publish', action='store_true', help='ZennAPI V2で記事を公開設定にする') 

    # Firefox 設定
    parser.add_argument('--firefox-binary-path', type=str, help='Firefox の実行ファイルへのパス')
    parser.add_argument('--firefox-profile-path', type=str, help='使用する Firefox プロファイルへのパス')
    parser.add_argument('--firefox-headless', action='store_true', help='Firefoxのヘッドレスモード')

    # Streamlitアプリオプション
    parser.add_argument('--webui', action='store_true', help='WebUIモードで起動する')

    args = parser.parse_args()

    if args.webui:
        import streamlit.web.cli as stcli
        oasis_webui_path = os.path.join(os.path.dirname(__file__), 'app/oasis_webui.py')
        sys.argv = ["streamlit", "run", oasis_webui_path, "--"]
        sys.exit(stcli.main())

    if not (args.folder or args.markdown) and not args.webui:
        parser.error("--folder または --markdown オプションが必要です")

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
        firefox_headless=args.firefox_headless,
        zenn_output_path=args.zenn_output_path,
        zenn_publish=args.zenn_publish
    )
    
    logger.info(
        f"使用中のLLMモデル: {oasis.config.LLM_MODEL}, 最大リトライ回数: {args.max_retries}"
    )

    if args.folder:
        result = oasis.process_folder(
            args.folder,
            post_to_qiita=args.qiita,
            post_to_note=args.note,
            post_to_wp=args.wp,
            post_to_zenn=args.zenn
        )
    else:
        result = oasis.process_files(
            args.markdown,
            args.image,
            post_to_qiita=args.qiita,
            post_to_note=args.note,
            post_to_wp=args.wp,
            post_to_zenn=args.zenn
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
