import argparse
import sys
from .oasis import OASIS
from .config import Config
from .logger import logger
from .services.oasis_runner import run_oasis
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
    parser.add_argument('--llm-model', type=str, default=Config.LLM_MODEL, help='使用するLLMモデル')
    parser.add_argument(
        '--max-retries', type=int, default=Config.MAX_RETRIES, help='LLMリクエストの最大リトライ回数'
    )
    
    # mode
    parser.add_argument('--qiita', action='store_true', help='Qiitaにも投稿する')
    parser.add_argument('--note', action='store_true', help='Noteにも投稿する')
    parser.add_argument('--wp', action='store_true', help='WordPressにも投稿する')
    parser.add_argument('--zenn', action='store_true', help='Zennにも投稿する')

    # wp
    parser.add_argument('--wp-user', type=str, default=Config.AUTH_USER, help='WordPressのユーザー名')
    parser.add_argument('--wp-pass', type=str, default=Config.AUTH_PASS, help='WordPressのパスワード')
    parser.add_argument('--wp-url', type=str, default=Config.BASE_URL, help='WordPressのURL')

    # qiita
    parser.add_argument('--qiita-token', type=str, default=Config.QIITA_TOKEN, help='QiitaのAPIトークン')
    parser.add_argument('--qiita-post-publish', action='store_true', default=Config.QIITA_POST_PUBLISH, help='Qiitaの公開設定')

    # note
    parser.add_argument('--note-email', type=str, default=Config.NOTE_EMAIL, help='Noteのメールアドレス')
    parser.add_argument('--note-password', type=str, default=Config.NOTE_PASSWORD, help='Noteのパスワード')
    parser.add_argument('--note-user-id', type=str, default=Config.NOTE_USER_ID, help='NoteのユーザーID')
    parser.add_argument('--note-publish', action='store_true', default=Config.NOTE_PUBLISH, help='公開するかどうか')
    parser.add_argument('--note-api-ver', type=str, default=Config.NOTE_API_VER, help='NoteのAPI Ver')
    
    # zenn
    parser.add_argument('--zenn-output-path', default=Config.ZENN_OUTPUT_PATH, help='ZennAPI V2の出力フォルダ')
    parser.add_argument('--zenn-publish', action='store_true', default=Config.ZENN_PUBLISH, help='ZennAPI V2で記事を公開設定にする')

    # Firefox 設定
    parser.add_argument('--firefox-binary-path', type=str, default=Config.FIREFOX_BINARY_PATH, help='Firefox の実行ファイルへのパス')
    parser.add_argument('--firefox-profile-path', type=str, default=Config.FIREFOX_PROFILE_PATH, help='使用する Firefox プロファイルへのパス')
    parser.add_argument('--firefox-headless', action='store_true', default=Config.FIREFOX_HEADLESS, help='Firefoxのヘッドレスモード')

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

    params = vars(args)
    run_oasis(params)


if __name__ == '__main__':
    main()
