<p align="center">
<img src="https://huggingface.co/datasets/MakiAi/IconAssets/resolve/main/OASIS.png" width="100%">
<br>
<h1 align="center"> O.A.S.I.S </h1>
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
  <a href="https://hamaruki.com/"><b>[ Website ]</b></a> •
  <a href="https://github.com/Sunwood-ai-labs"><b>[ GitHub ]</b></a>
  <a href="https://x.com/hAru_mAki_ch"><b>[ Twitter ]</b></a> •
  <a href="https://hamaruki.com/"><b>[ Official Blog ]</b></a>
</p>
   <br>
   <a href="https://github.com/Sunwood-ai-labs/OASIS/blob/main/README.md"><img src="https://img.shields.io/badge/ドキュメント-日本語-white.svg" alt="JA doc"/></a>
   <a href="https://github.com/Sunwood-ai-labs/OASIS/blob/main/docs/README.en.md"><img src="https://img.shields.io/badge/english-document-white.svg" alt="EN doc"></a>
</h2>

</p>

>[!IMPORTANT]
>このリポジトリのリリースノートやREADME、コミットメッセージの9割近くは[claude.ai](https://claude.ai/)や[ChatGPT4](https://chatgpt.com/)を活用した[AIRA](https://github.com/Sunwood-ai-labs/AIRA), [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage), [Gaiah](https://github.com/Sunwood-ai-labs/Gaiah), [HarmonAI_II](https://github.com/Sunwood-ai-labs/HarmonAI_II)で生成しています。

OASISは、MarkdownファイルからWordPress, Qiita, Note, Zennへの投稿を自動化するPythonパッケージです。 

## 更新情報 

- **v0.9.3**: 
  - 英語READMEの更新と、コマンドラインオプションの説明の改善
  - 詳しくは[リリースノート](https://github.com/Sunwood-ai-labs/OASIS/releases/tag/v0.9.3)をご覧ください。
- **v0.9.2**: 
  - Zenn API V2 への公開設定機能、Instagram自動投稿機能(実験的機能)の強化、新しいタグの追加、README翻訳のワークフロー、およびその他の改善が含まれています。
  - 詳しくは[リリースノート](https://github.com/Sunwood-ai-labs/OASIS/releases/tag/v0.9.2)をご覧ください。

<details>
  <summary>過去の更新情報はこちら</summary>

  ---
- **v0.8.0**: 
  - StreamlitベースのWeb UIを追加しました。
  - コマンドラインインターフェースを改善し、Streamlitアプリケーション起動オプションを追加しました。
  - AI関連の新しいカテゴリとタグを追加しました。
  - 詳しくは[リリースノート](https://github.com/Sunwood-ai-labs/OASIS/releases/tag/v0.8.0)をご覧ください。
- **v0.7.0**: 
  - Zennへのクロス投稿機能を追加しました。 
  - WordPressとNoteにおけるMermaid図のレンダリングに対応しました。
  - 詳しくは[リリースノート](https://github.com/Sunwood-ai-labs/OASIS/releases/tag/v0.7.0)をご覧ください。
- **v0.6.0**: 
  - Zennへのクロス投稿機能を追加しました。 
  - WordPressとNoteにおけるMermaid図のレンダリングに対応しました。
  - 詳しくは[リリースノート](https://github.com/Sunwood-ai-labs/OASIS/releases/tag/v0.6.0)をご覧ください。
- **v0.5.0**: 
  - リンクプレビュー生成機能にiframelyサポートを追加しました。(実験的機能)
  - Note API v2では、HTMLを直接挿入することで、従来の方法よりも高速にコンテンツを投稿できるようになりました。
  - 詳しくは[リリースノート](https://github.com/Sunwood-ai-labs/OASIS/releases/tag/v0.5.0)をご覧ください。
- **v0.4.3**: Noteへの投稿機能を大幅に改善しました。
  - マークダウンのより多くの要素に対応しました。
  - 詳しくは[リリースノート](https://github.com/Sunwood-ai-labs/OASIS/releases/tag/v0.4.3)をご覧ください。
- **v0.4.0**: Noteへのクロス投稿機能を追加しました。MarkdownファイルからNoteへの記事投稿を自動化し、複数のプラットフォームでコンテンツを簡単に共有できます。 詳しくは[リリースノート](https://github.com/Sunwood-ai-labs/OASIS/releases/tag/v0.4.0)をご覧ください。
- **過去のバージョン情報はこちら:** [Releases](https://github.com/Sunwood-ai-labs/OASIS/releases)
</details>

  ---

## デモ

### CLI デモ

https://github.com/user-attachments/assets/742c5822-04ec-4f9b-98fb-42fc3a101ab6

### Web UI デモ

https://github.com/user-attachments/assets/ff0a2099-dcd0-4fe5-b60b-ded3f2f55fe4

## はじめに

OASISを使用すると、MarkdownファイルからWordPress, Qiita, Note, Zennへの投稿を効率的に行うことができます。LLMによる自動カテゴリ・タグ提案やサムネイル画像の自動アップロードなど、便利な機能が満載です。

## インストール

```bash
pip install -U oasis-article
```

## 使用方法

### コマンドラインから使用する場合:

```bash
oasis --folder_path /path/to/your/folder
```

### オプション

OASISは多数のオプションを提供し、様々な設定や機能をカスタマイズできます。以下は主要なオプションの一覧です：

#### 基本オプション
- `--folder_path`: 処理するフォルダのパス（必須）
- `-app`, `--streamlit-app`: StreamlitベースのWeb UIを起動する

#### 投稿先の指定
- `--qiita`: Qiitaにも投稿する
- `--note`: Noteにも投稿する
- `--wp`: WordPressにも投稿する
- `--zenn`: Zennにも投稿する

#### WordPress設定
- `--wp-user`: WordPressのユーザー名
- `--wp-pass`: WordPressのパスワード
- `--wp-url`: WordPressのURL

#### Qiita設定
- `--qiita-token`: QiitaのAPIトークン
- `--qiita-post-publish`: Qiitaの記事を公開設定で投稿する（指定しない場合は非公開で投稿）

#### Note設定
- `--note-email`: Noteのメールアドレス
- `--note-password`: Noteのパスワード
- `--note-user-id`: NoteのユーザーID
- `--note-publish`: Noteに公開投稿する(指定しない場合は下書き保存)

#### Zenn設定
- `--zenn-output-path`: ZennAPI V2で記事ファイルを生成する出力フォルダ
- `--zenn-publish`: ZennAPI V2で記事を公開設定にする

#### Firefox設定
- `--firefox-binary-path`: Firefox の実行ファイルへのパス
- `--firefox-profile-path`: 使用する Firefox プロファイルへのパス
- `--firefox-headless`: Firefoxのヘッドレスモード

#### その他
- `--llm-model`: 使用するLLMモデル
- `--max-retries`: LLMリクエストの最大リトライ回数

### 使用例

```bash
oasis --folder_path example\article\roomba01 --qiita --qiita-post-publish --note --wp --zenn --firefox-headless
oasis --folder_path article_draft\21_Hunk --qiita --note --wp --zenn --firefox-headless
```

### Pythonスクリプトから使用する場合:

```python
from oasis import OASIS

oasis = OASIS()
result = oasis.process_folder("/path/to/your/folder", post_to_qiita=True, post_to_note=True, post_to_wp=True, post_to_zenn=True)  # Qiita, Note, WordPress, Zennへの投稿も行う場合
print(result)
```

### Web UIを使用する場合:

```bash
oasis -app
```

または

```bash
oasis --streamlit-app
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

## ZennAPI V2 について

ZennAPI V2 は、Zenn と GitHub の連携を活用して動作します。 `--zenn-output-path` オプションで指定したフォルダに、Zenn の記事ファイル (.md) を生成します。 生成された記事ファイルを GitHub リポジトリにプッシュすると、Zenn 上で記事が公開されます。

## コントリビューション

OASISの開発にご協力いただける方は、GitHubリポジトリにアクセスしてください。Issue報告、プルリクエストをお待ちしております。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。 

## 謝辞

OASISの開発にあたり、多大な貢献をしていただいた方々に感謝申し上げます。

- Note APIの開発は [Mr-SuperInsane/NoteClient](https://github.com/Mr-SuperInsane/NoteClient) を参考にさせていただきました。

## Docker Composeでの起動 🐳

Docker Composeを使用してOASISのWeb UIを簡単にコンテナ起動できます。
ルートディレクトリに`.env`ファイルを配置し、必要な環境変数を設定した上で、以下のコマンドを実行してください:

```bash
docker-compose up --build
```

起動後、ブラウザで [http://localhost:8501](http://localhost:8501) にアクセスするとWeb UIが表示されます。
CLIコマンドを実行する場合は、以下のように実行できます:
```bash
docker-compose run --rm oasis --help
```

</readme>
```