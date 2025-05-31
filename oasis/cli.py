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

    params = vars(args)
    run_oasis(params)


if __name__ == '__main__':
    main()
