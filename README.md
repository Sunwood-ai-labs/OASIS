<p align="center">
<img src="https://huggingface.co/datasets/MakiAi/IconAssets/resolve/main/OASIS.png" width="100%">
<br>
<h1 align="center">O.A.S.I.S</h1>
<h2 align="center">
  ～ Optimized Article Sorting Intelligent System ～
<br>
  <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/oasis-article">
<img alt="PyPI - Format" src="https://img.shields.io/pypi/format/oasis-article">
<img alt="PyPI - Implementation" src="https://img.shields.io/pypi/implementation/oasis-article">
<img alt="PyPI - Status" src="https://img.shields.io/pypi/status/oasis-article">
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dd/oasis-article">
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dw/oasis-article">
<a href="https://github.com/Sunwood-ai-labs/OASIS" title="Go to GitHub repo"><img src="https://img.shields.io/static/v1?label=OASIS&message=Sunwood-ai-labs&color=blue&logo=github"></a>
<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/Sunwood-ai-labs/OASIS">
<a href="https://github.com/Sunwood-ai-labs/OASIS"><img alt="forks - Sunwood-ai-labs" src="https://img.shields.io/github/forks/OASIS/Sunwood-ai-labs?style=social"></a>
<a href="https://github.com/Sunwood-ai-labs/OASIS"><img alt="GitHub Last Commit" src="https://img.shields.io/github/last-commit/Sunwood-ai-labs/OASIS"></a>
<a href="https://github.com/Sunwood-ai-labs/OASIS"><img alt="GitHub Top Language" src="https://img.shields.io/github/languages/top/Sunwood-ai-labs/OASIS"></a>
<img alt="GitHub Release" src="https://img.shields.io/github/v/release/Sunwood-ai-labs/OASIS?color=red">
<img alt="GitHub Tag" src="https://img.shields.io/github/v/tag/Sunwood-ai-labs/OASIS?sort=semver&color=orange">
<img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/Sunwood-ai-labs/OASIS/publish-to-pypi.yml">
<br>
<p align="center">
  <a href="https://hamaruki.com/"><b>[ Website]</b></a> •
  <a href="https://github.com/Sunwood-ai-labs"><b>[ GitHub]</b></a>
  <a href="https://x.com/hAru_mAki_ch"><b>[ Twitter]</b></a> •
  <a href="https://hamaruki.com/"><b>[ Official Blog]</b></a>
</p>

</h2>

</p>

>[!IMPORTANT]
>このリポジトリのリリースノートやREADME、コミットメッセージの9割近くは[claude.ai](https://claude.ai/)や[ChatGPT4](https://chatgpt.com/)を活用した[AIRA](https://github.com/Sunwood-ai-labs/AIRA), [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage), [Gaiah](https://github.com/Sunwood-ai-labs/Gaiah), [HarmonAI_II](https://github.com/Sunwood-ai-labs/HarmonAI_II)で生成しています。

## O.A.S.I.S (Optimized Article Sorting Intelligent System)

～ 最適化された記事分類インテリジェントシステム ～

OASISは、MarkdownファイルからWordPress, Qiita, Noteへの投稿を自動化するPythonパッケージです。

## 更新情報

- **v0.5.0**: 
  - リンクプレビュー生成機能にiframelyサポートを追加しました。(実験的機能)
  - Note API v2では、HTMLを直接挿入することで、従来の方法よりも高速にコンテンツを投稿できるようになりました。
  - 詳しくは[リリースノート](https://github.com/Sunwood-ai-labs/OASIS/releases/tag/v0.5.0)をご覧ください。
- **v0.4.3**: Noteへの投稿機能を大幅に改善しました。
  - マークダウンのより多くの要素に対応しました。
  - 詳しくは[リリースノート](https://github.com/Sunwood-ai-labs/OASIS/releases/tag/v0.4.3)をご覧ください。
- **v0.4.0**: Noteへのクロス投稿機能を追加しました。MarkdownファイルからNoteへの記事投稿を自動化し、複数のプラットフォームでコンテンツを簡単に共有できます。 詳しくは[リリースノート](https://github.com/Sunwood-ai-labs/OASIS/releases/tag/v0.4.0)をご覧ください。
- **過去のバージョン情報はこちら:** [Releases](https://github.com/Sunwood-ai-labs/OASIS/releases)

## デモ


## はじめに

OASISを使用すると、MarkdownファイルからWordPress, Qiita, Noteへの投稿を効率的に行うことができます。LLMによる自動カテゴリ・タグ提案やサムネイル画像の自動アップロードなど、便利な機能が満載です。

## インストール

```bash
pip install -U oasis-article
```

## 使用方法

### コマンドラインから使用する場合:

```bash
oasis /path/to/your/folder
```

#### オプション

- `--qiita`: Qiitaにも投稿する
- `--note`: Noteにも投稿する
- `--wp`: WordPressにも投稿する
- `--wp-user`: WordPressのユーザー名
- `--wp-pass`: WordPressのパスワード
- `--wp-url`: WordPressのURL
- `--qiita-token`: QiitaのAPIトークン
- `--note-email`: Noteのメールアドレス
- `--note-password`: Noteのパスワード
- `--note-user-id`: NoteのユーザーID
- `--note-publish`: Noteに公開投稿する(指定しない場合は下書き保存)
- `--firefox-binary-path`: Firefox の実行ファイルへのパス
- `--firefox-profile-path`: 使用する Firefox プロファイルへのパス
- `--firefox-headless`: Firefoxのヘッドレスモード

例：

```bash
oasis example\article\roomba01 --qiita --note --wp
```

### Pythonスクリプトから使用する場合:

```python
from oasis import OASIS

oasis = OASIS()
result = oasis.process_folder("/path/to/your/folder", post_to_qiita=True, post_to_note=True, post_to_wp=True)  # Qiita, Note, WordPressへの投稿も行う場合
print(result)
```

## 設定

環境変数を使用して設定を行います:
[.env.example](.env.example)を参考にしてください。

- `AUTH_USER`: WordPressのユーザー名
- `AUTH_PASS`: WordPressのパスワード
- `BASE_URL`: WordPressサイトのURL
- `LLM_MODEL`: 使用するLLMモデル（デフォルト: "gemini/gemini-1.5-pro-latest"）
- `QIITA_TOKEN`: QiitaのAPIトークン（Qiitaへの投稿を行う場合に必要）
- `NOTE_EMAIL`: Noteのアカウントに関連付けられたメールアドレス
- `NOTE_PASSWORD`: Noteアカウントのパスワード
- `NOTE_USER_ID`: NoteのユーザーID
- `FIREFOX_BINARY_PATH`: Firefox の実行ファイルへのパス (任意)
- `FIREFOX_PROFILE_PATH`: 使用する Firefox プロファイルへのパス (任意)

## サンプルスクリプト

`example/script`フォルダには、OASISの様々な機能を試すためのサンプルスクリプトが用意されています。

- `demo_note_api.py`: Note API v1を使用してNoteに記事を投稿するサンプルスクリプト
- `demo_note_api_v2.py`: Note API v2を使用してNoteに記事を投稿するサンプルスクリプト
- `demo_qiita_api.py`: Qiita APIを使用してQiitaに記事を投稿するサンプルスクリプト
- `demo_url2card.py`: URLからWebサイトカードを生成するサンプルスクリプト

これらのスクリプトは、OASISの機能を理解し、実際に試してみるための良い出発点となります。


## コントリビューション

OASISの開発にご協力いただける方は、GitHubリポジトリにアクセスしてください。Issue報告、プルリクエストをお待ちしております。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。 

## 謝辞

OASISの開発にあたり、多大な貢献をしていただいた方々に感謝申し上げます。

- Note APIの開発は [Mr-SuperInsane/NoteClient](https://github.com/Mr-SuperInsane/NoteClient) を参考にさせていただきました。
