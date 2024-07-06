import os
from dotenv import load_dotenv
import sys

# プロジェクトのルートディレクトリをパスに追加
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from oasis import NoteAPIV2

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数から値を取得
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
USER_ID = os.getenv('USER_ID')

# スクリプト内で直接定義する値
TITLE = 'Jetson'
CONTENT_PATH = 'content.md'
CONTENT_PATH = r'draft\jet03\README.md'
TAG_LIST = ['sample_tag']
IMAGE_INDEX = 0  # 変数名を修正
POST_SETTING = True
HEADLESS = False

# NoteClient のインスタンスを作成
note = NoteAPIV2(email=EMAIL, password=PASSWORD, user_id=USER_ID)

# 記事を作成
result = note.create_article(
    title=TITLE,
    input_tag_list=TAG_LIST,  # 引数名を修正
    # image_index=IMAGE_INDEX,  # 引数名を修正
    post_setting=POST_SETTING,  # 引数名を修正
    file_name=CONTENT_PATH,
    headless=HEADLESS
)

print(result)
