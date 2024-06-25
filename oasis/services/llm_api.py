from litellm import completion
from ..logger import logger
from ..config import Config
from ..exceptions import APIError
import json
import re

class LLMService:
    def __init__(self, max_retries=3):
        self.model = Config.LLM_MODEL
        self.max_retries = max_retries
        logger.info(f"LLMモデルを初期化: {self.model}, 最大リトライ回数: {self.max_retries}")

    def _get_completion_with_retry(self, prompt):
        for attempt in range(self.max_retries):
            try:
                logger.info(f"LLMにリクエストを送信中: {self.model} (試行 {attempt + 1}/{self.max_retries})")
                response = completion(model=self.model, messages=[{"role": "user", "content": prompt}])
                content = response.choices[0].message.content
                logger.info(f"content: \n{content}")

                # コードブロックの抽出
                code_block_pattern = r'```(?:json)?([\s\S]*?)```'
                code_blocks = re.findall(code_block_pattern, content, re.DOTALL)

                if code_blocks:
                    # 最後のコードブロックを使用
                    json_content = code_blocks[-1].strip()
                else:
                    # コードブロックがない場合は全体を使用
                    json_content = content

                # JSONとしてパースを試みる
                json.loads(json_content)
                return json_content
            except json.JSONDecodeError:
                logger.warning(f"LLMの応答がJSONではありません。リトライします。(試行 {attempt + 1}/{self.max_retries})")
            except Exception as e:
                logger.error(f"LLMリクエスト中にエラーが発生: {str(e)}")
                raise APIError(f"LLMリクエスト中にエラーが発生: {str(e)}")
        
        raise APIError(f"LLMからの有効な応答の取得に失敗しました。{self.max_retries}回試行しました。")

    def suggest_categories_and_tags(self, content, existing_categories, existing_tags):
        logger.info("カテゴリとタグの提案を開始")
        prompt = f"""
        既存カテゴリ: {', '.join(existing_categories)}
        既存タグ: {', '.join(existing_tags)}

        この記事に最適で、シンプルで、簡潔なカテゴリとタグを提案してください：
        - 既存の類似カテゴリやタグがあれば、それを優先して使用
        - 必要な場合のみ新しいものを提案
        - カテゴリは大きな分類、タグは小さな分類
        - タグにカテゴリを含めない
        - 名前とslugを含める
        - slugはシンプルな英語にする
        - 平易な言葉を使う
        - 下記のJSONフォーマットで回答する

        記事:
        {content[:1000]}

        JSONで回答：
        {{
            "categories": [
                {{"name": "カテゴリ名1", "slug": "categories-slug1"}},
                {{"name": "カテゴリ名2", "slug": "categories-slug2"}},
                ...
            ],
            "tags": [
                {{"name": "タグ名1", "slug": "tag-slug1"}},
                {{"name": "タグ名2", "slug": "tag-slug2"}},
                ...
            ]
        }}
        """
        response = self._get_completion_with_retry(prompt)
        logger.success("カテゴリとタグの提案が完了")

        return json.loads(response)

    def generate_english_slug(self, title):
        logger.info("英語のスラグ生成を開始")
        prompt = f"""
        以下の日本語のタイトルを英語に翻訳し、WordPressのslugとして適切な形式に変換してください。
        slugは短く、簡潔で、URLに適した形式にしてください。

        日本語タイトル: {title}

        回答は以下のJSONフォーマットで提供してください：
        {{
            "slug": "英語のslug"
        }}
        """
        response = self._get_completion_with_retry(prompt)
        logger.info("英語のスラグ生成が完了")
        result = json.loads(response)
        return result['slug']
