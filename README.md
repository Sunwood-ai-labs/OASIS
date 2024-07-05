<p align="center">
<img src="https://huggingface.co/datasets/MakiAi/IconAssets/resolve/main/OASIS.png" width="100%">
<br>
<h1 align="center">OASIS</h1>
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
  <a href="https://hamaruki.com/"><b>[🌐 Website]</b></a> •
  <a href="https://github.com/Sunwood-ai-labs"><b>[🐱 GitHub]</b></a>
  <a href="https://x.com/hAru_mAki_ch"><b>[🐦 Twitter]</b></a> •
  <a href="https://hamaruki.com/"><b>[🍀 Official Blog]</b></a>
</p>

</h2>

</p>

>[!IMPORTANT]
>このリポジトリのリリースノートやREADME、コミットメッセージの9割近くは[claude.ai](https://claude.ai/)や[ChatGPT4](https://chatgpt.com/)を活用した[AIRA](https://github.com/Sunwood-ai-labs/AIRA), [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage), [Gaiah](https://github.com/Sunwood-ai-labs/Gaiah), [HarmonAI_II](https://github.com/Sunwood-ai-labs/HarmonAI_II)で生成しています。

## 🌟 O.A.S.I.S (Optimized Article Sorting Intelligent System)

～ 最適化された記事分類インテリジェントシステム ～

OASISは、MarkdownファイルからWordPressへの投稿を自動化するPythonパッケージです。v0.3.0からは、Qiitaへのクロス投稿機能も追加されました！

## 🎥 デモ

※ デモ動画があればここに埋め込み

## 🚀 はじめに

OASISを使用すると、MarkdownファイルからWordPressとQiitaへの投稿を効率的に行うことができます。LLMによる自動カテゴリ・タグ提案やサムネイル画像の自動アップロードなど、便利な機能が満載です。

## インストール

```bash
pip install -U oasis-article
```

## 使用方法

### コマンドラインから使用する場合:

```bash
oasis /path/to/your/folder
```

WordPressとQiitaの両方に投稿する場合:

```bash
oasis /path/to/your/folder --qiita
```

例：

```bash
oasis articles_draft/ELYZA-tasks-100-v2 --qiita
```

### Pythonスクリプトから使用する場合:

```python
from oasis import OASIS

oasis = OASIS()
result = oasis.process_folder("/path/to/your/folder", post_to_qiita=True)  # Qiitaへの投稿も行う場合
print(result)
```

## 📝 設定

環境変数を使用して設定を行います:

- `AUTH_USER`: WordPressのユーザー名
- `AUTH_PASS`: WordPressのパスワード
- `BASE_URL`: WordPressサイトのURL
- `LLM_MODEL`: 使用するLLMモデル（デフォルト: "gemini/gemini-1.5-pro-latest"）
- `QIITA_TOKEN`: QiitaのAPIトークン（Qiitaへの投稿を行う場合に必要）

## 🆕 新機能 (v0.3.0)

- **Qiitaへのクロス投稿機能**: WordPressへの投稿と同時に、Qiitaにも記事を投稿できるようになりました。
- **CLIオプションの追加**: `--qiita`オプションを使用してQiitaへの投稿を有効化できます。
- **Qiita API統合**: Qiita APIとの通信を処理する専用のサービス層を追加しました。
- **エラーハンドリングの改善**: APIエラーが発生した際にデバッグ情報を保存する機能を追加しました。

## 🤝 コントリビューション

OASISの開発にご協力いただける方は、GitHubリポジトリにアクセスしてください。Issue報告、プルリクエストをお待ちしております。

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。 

## 🙏 謝辞

OASISの開発にあたり、多大な貢献をしていただいた方々に感謝申し上げます。
