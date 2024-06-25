## 🌟 O.A.S.I.S (Optimized Article Sorting Intelligent System)

～ 最適化された記事分類インテリジェントシステム ～

OASISは、MarkdownファイルからWordPressへの投稿を自動化するPythonパッケージです。

## 🎥 デモ

※ デモ動画があればここに埋め込み

## 🚀 はじめに

OASISを使用すると、MarkdownファイルからWordPressへの投稿を効率的に行うことができます。LLMによる自動カテゴリ・タグ提案やサムネイル画像の自動アップロードなど、便利な機能が満載です。

## インストール

```bash
pip install oasis-article
```

## 使用方法

### コマンドラインから使用する場合:

```bash
oasis /path/to/your/folder
```

例：

```bash
oasis articles_draft/ELYZA-tasks-100-v2
```

### Pythonスクリプトから使用する場合:

```python
from oasis import OASIS

oasis = OASIS()
result = oasis.process_folder("/path/to/your/folder")
print(result)
```

## 📝 設定

環境変数を使用して設定を行います:

- `AUTH_USER`: WordPressのユーザー名
- `AUTH_PASS`: WordPressのパスワード
- `BASE_URL`: WordPressサイトのURL
- `LLM_MODEL`: 使用するLLMモデル（デフォルト: "gemini/gemini-1.5-pro-latest"）

## 🤝 コントリビューション

OASISの開発にご協力いただける方は、GitHubリポジトリにアクセスしてください。Issue報告、プルリクエストをお待ちしております。

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。 

## 🙏 謝辞

OASISの開発にあたり、多大な貢献をしていただいた方々に感謝申し上げます。
