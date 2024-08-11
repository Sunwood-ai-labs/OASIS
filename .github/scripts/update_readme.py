import os
import sys

# Add the parent directory of 'scripts' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from github import Github
from loguru import logger
from config import get_settings
from services.llm_service import LLMService

def main():
    logger.info("README更新プロセスを開始します。")
    
    settings = get_settings()
    llm_service = LLMService()
    g = Github(settings.YOUR_PERSONAL_ACCESS_TOKEN_IRIS)
    repo = g.get_repo(settings.GITHUB_REPOSITORY)

    # 最新のリリースを取得
    latest_release = repo.get_latest_release()
    logger.info(f"最新のリリース: {latest_release.title}")

    # READMEの内容を取得
    readme = repo.get_contents("README.md")
    readme_content = readme.decoded_content.decode("utf-8")
    
    repo_summary_path = ".SourceSageAssets/DOCUMIND/Repository_summary.md"
    repo_summary_content = ""

    # リポジトリのサマリーファイルをローカルから読み込む
    try:
        with open(repo_summary_path, 'r', encoding='utf-8') as f:
            repo_summary_content = f.read()
        logger.info("リポジトリのサマリーファイルを読み込みました。")
    except FileNotFoundError:
        logger.warning(f"リポジトリのサマリーファイルが見つかりません: {repo_summary_path}")
    except Exception as e:
        logger.warning(f"リポジトリのサマリーファイルの読み込みに失敗しました: {str(e)}")

    # LLMにプロンプトを送信

    prompt = f"""
以下の情報を元に、下記の更新のガイドラインに従って既存のREADMEを更新してください：
各セクションはHTMLのタグで囲ってあります。

# 更新のガイドライン:
<Update guidelines>
1. 最新のリリースで追加された主要な機能や重要な変更点のみをREADME内の適切な位置に簡潔に記載してください。
2. 詳細な更新情報の記載は不要で、コミットハッシュなどは不要で、代わりに「![v1.11.1](https://github.com/Sunwood-ai-labs/AlphaExperiment/releases/tag/v1.11.1)」のようなリリースノートのURLを記載しておいて。
2. 既存の構造を維持しつつ、必要な箇所のみを更新してください。
3. 読みやすく、理解しやすい日本語で記述してください。
4. 絵文字は適度に使用し、読みやすさを損なわないようにしてください。
5. リポジトリ中身を深く観察し存在しないファイルへのパスは記載しないで
6. READMEの上にリリースノートを付けるような形式ではなく、READMEの中身の各章を更新する形式で更新してください。
更新されたREADMEの全文をそのまま出力してください。
7. リポジトリの全体情報を加味してREADMEを更新して
8. READMEへの更新情報への記載は1つのリリースノートにつき1行で簡潔にまとめて記載して。

</Update guidelines>

# 最新のリリース情報:
<Latest release information>
バージョン: {latest_release.title}
主な変更点:
{latest_release.body}
</Latest release information>

# 更新して欲しいREADME:
<readme>
{readme_content}
</readme>

# [参考資料] リポジトリの全体情報
下記にはリポジトリの構造とリポジトリ内の主要なファイルの一覧を記載します。
リリースノートを作成時の事前知識として参考に使用して

<Repository information>
    {repo_summary_content}
</Repository information>

    """

    logger.info("LLMに更新を依頼しています...")
    logger.info(f"プロンプト：\n{prompt}")
    updated_readme = llm_service.get_response(prompt, remove_code_block=True)

    logger.info(f">> updated_readme：\n{updated_readme}")
    
    # 更新されたREADMEの内容をファイルに書き込む
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated_readme)

    logger.info("READMEの更新が完了しました。")

if __name__ == "__main__":
    main()
