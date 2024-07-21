import requests
import json
from loguru import logger
from dotenv import load_dotenv
import os
import time

# .envファイルから環境変数を読み込む
load_dotenv()

# アクセストークンを環境変数から取得
ACCESS_TOKEN = os.getenv("QIITA_ACCESS_TOKEN")

# APIのベースURL
BASE_URL = "https://qiita.com/api/v2"

# 共通のヘッダー
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def post_article():
    """新しい記事を投稿する"""
    endpoint = f"{BASE_URL}/items"
    data = {
        "title": "テスト投稿",
        "body": "# これはテスト投稿です\n\nQiita API v2を使用して投稿しています。",
        "private": True,
        "tags": [{"name": "Python"}, {"name": "Qiita"}]
    }
    try:
        response = requests.post(endpoint, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        logger.info(f"投稿ステータス: {response.status_code}")
        logger.debug(f"レスポンスヘッダー: {response.headers}")
        logger.debug(f"レスポンス本文: {response.text}")
        return response.json()['id']
    except requests.exceptions.RequestException as e:
        logger.error(f"投稿エラー: {e}")
        logger.debug(f"リクエストURL: {e.request.url}")
        logger.debug(f"リクエストヘッダー: {e.request.headers}")
        logger.debug(f"リクエスト本文: {e.request.body}")
        if e.response:
            logger.debug(f"レスポンスステータス: {e.response.status_code}")
            logger.debug(f"レスポンスヘッダー: {e.response.headers}")
            logger.debug(f"レスポンス本文: {e.response.text}")
        return None

def get_article(article_id):
    """指定したIDの記事を取得する"""
    endpoint = f"{BASE_URL}/items/{article_id}"
    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        logger.info(f"取得ステータス: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"取得エラー: {e}")
        return None

def update_article(article_id):
    """指定したIDの記事を更新する"""
    endpoint = f"{BASE_URL}/items/{article_id}"
    data = {
        "title": "更新されたテスト投稿",
        "body": "# これは更新されたテスト投稿です\n\nQiita API v2を使用して更新しました。",
    }
    try:
        response = requests.patch(endpoint, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        logger.info(f"更新ステータス: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"更新エラー: {e}")
        return None

def delete_article(article_id):
    """指定したIDの記事を削除する"""
    endpoint = f"{BASE_URL}/items/{article_id}"
    try:
        response = requests.delete(endpoint, headers=headers)
        response.raise_for_status()
        logger.info(f"削除ステータス: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"削除エラー: {e}")
        return False

def main():
    logger.info("Qiita API操作を開始します")

    # 新しい記事を投稿
    article_id = post_article()
    if article_id:
        logger.success(f"投稿された記事ID: {article_id}")

        # 投稿後に少し待機
        logger.info("投稿後5秒間待機します...")
        time.sleep(5)

        # 投稿した記事を取得
        article = get_article(article_id)
        if article:
            logger.success(f"取得した記事のタイトル: {article['title']}")
        else:
            logger.warning("記事の取得に失敗しました")

        # # 記事を更新
        # updated_article = update_article(article_id)
        # if updated_article:
        #     logger.success(f"更新後の記事タイトル: {updated_article['title']}")
        # else:
        #     logger.warning("記事の更新に失敗しました")

        # # 記事を削除
        # if delete_article(article_id):
        #     logger.success("記事が正常に削除されました")
        # else:
        #     logger.error("記事の削除に失敗しました")
    else:
        logger.error("記事の投稿に失敗しました")

    logger.info("Qiita API操作を終了します")

if __name__ == "__main__":
    main()

    # article_id = "253e1367282fda40d205"
    # # 投稿した記事を取得
    # article = get_article(article_id)
    # if article:
    #     logger.success(f"取得した記事のタイトル: {article['title']}")
    # else:
    #     logger.warning("記事の取得に失敗しました")

