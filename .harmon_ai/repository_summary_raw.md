## O.A.S.I.S (Optimized Article Sorting Intelligent System)

～ 最適化された記事分類インテリジェントシステム ～

OASISは、MarkdownファイルからWordPressへの投稿を自動化するPythonパッケージです。

## 特徴

- Markdownファイルの自動処理
- LLMを使用したカテゴリとタグの自動提案
- サムネイル画像の自動アップロード
- 柔軟なLLMモデルの選択

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

## 設定

環境変数を使用して設定を行います:

- `AUTH_USER`: WordPressのユーザー名
- `AUTH_PASS`: WordPressのパスワード
- `BASE_URL`: WordPressサイトのURL
- `LLM_MODEL`: 使用するLLMモデル（デフォルト: "gemini/gemini-1.5-pro-latest"）

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。 
