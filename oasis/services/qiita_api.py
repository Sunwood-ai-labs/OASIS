import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime
from art import *

try:
    from ..logger import logger
    from ..exceptions import APIError
except:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from logger import logger
    from exceptions import APIError

class QiitaAPI:
    def __init__(self, token, post_private=True, post_tweet=False):
        self.token = token
        self.base_url = "https://qiita.com/api/v2"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        self.post_private = post_private
        self.post_tweet = post_tweet

    def create_post(self, post):
        tprint('>>  QiitaAPI')
        try:
            url = f"{self.base_url}/items"
            
            # タグの処理: 空白を削除し、最大5つまでに制限
            tags = [{"name": tag['name'].strip().replace(" ", "")} for tag in post.tags if tag['name'].strip()]
            tags = tags[:5]  # 最大5つのタグに制限
            
            payload = {
                "title": post.title[:100],  # タイトルを100文字に制限
                "body": post.content[:100000],  # 本文を100000文字に制限
                "tags": tags,
                "private": self.post_private,
                "tweet": self.post_tweet
            }
            
            response = requests.post(url, json=payload, headers=self.headers)
            
            if response.status_code != 201:
                logger.error(f"Qiita投稿の作成に失敗しました。ステータスコード: {response.status_code}")
                logger.error(f"レスポンス: {response.text}")
                self.save_error_payload(payload, response)
                raise APIError(f"Qiita投稿の作成に失敗しました。ステータスコード: {response.status_code}")
            
            logger.info("Qiita投稿が正常に作成されました。")
            return response.json()['id']
        except Exception as e:
            logger.error(f"Qiita投稿の作成中にエラーが発生しました: {str(e)}")
            self.save_error_payload(payload, response if 'response' in locals() else None)
            raise APIError(f"Qiita投稿の作成に失敗しました: {str(e)}")

    def save_error_payload(self, payload, response=None):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"qiita_error_{timestamp}.json"
        error_data = {
            "payload": payload,
            "response": {
                "status_code": response.status_code if response else None,
                "content": response.text if response else None
            } if response else None
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(error_data, f, ensure_ascii=False, indent=2)
        logger.info(f"エラー情報を {filename} に保存しました。")

    def get_authenticated_user(self):
        """認証されたユーザーの情報を取得"""
        url = f"{self.base_url}/authenticated_user"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"認証されたユーザー情報の取得に失敗しました: {str(e)}")
            raise APIError(f"認証されたユーザー情報の取得に失敗しました: {str(e)}")

if __name__ == "__main__":
    # .envファイルから環境変数を読み込む
    load_dotenv()

    # 環境変数からQiitaトークンを取得
    qiita_token = os.getenv('QIITA_TOKEN')

    if not qiita_token:
        print("エラー: QIITA_TOKENが設定されていません。.envファイルを確認してください。")
        sys.exit(1)

    # QiitaAPIのインスタンスを作成
    qiita_api = QiitaAPI(qiita_token)

    # 認証確認
    try:
        user_info = qiita_api.get_authenticated_user()
        print(f"認証成功: ユーザー名 {user_info['name']}")
    except APIError as e:
        print(f"認証失敗: {str(e)}")
        sys.exit(1)

    # テスト用の投稿データ
    class TestPost:
        def __init__(self):
            self.title = "OASISからのテスト投稿"
            self.content = "これはOASISを使用してQiitaに投稿するテストです。" * 10  # 内容を少し長くする
            self.tags = [{"name": "OASIS"}, {"name": "テスト"}, {"name": " Python "}, {"name": "API"}]

    test_post = TestPost()

    try:
        # テスト投稿の作成
        post_id = qiita_api.create_post(test_post)
        print(f"テスト投稿が成功しました。投稿ID: {post_id}")
    except APIError as e:
        print(f"テスト投稿に失敗しました: {str(e)}")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {str(e)}")
