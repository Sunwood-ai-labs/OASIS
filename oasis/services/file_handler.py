import os
from ..logger import logger
from ..exceptions import FileProcessingError

class FileHandler:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def read_markdown(self):
        try:
            markdown_files = [f for f in os.listdir(self.folder_path) if f.endswith('.md')]
            if not markdown_files:
                raise FileProcessingError("Markdownファイルが見つかりません。")
            
            markdown_path = os.path.join(self.folder_path, markdown_files[0])
            with open(markdown_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # タイトルを抽出（最初の#で始まる行）
            lines = content.split('\n')
            title = next((line.strip('# ') for line in lines if line.startswith('#')), "デフォルトタイトル")
            # タイトル行を除いたコンテンツ
            content = '\n'.join(line for line in lines if not line.startswith('#'))

            return content.strip(), title

        except Exception as e:
            logger.error(f"Markdownファイルの読み込み中にエラーが発生しました: {str(e)}")
            raise FileProcessingError(f"Markdownファイルの読み込みに失敗しました: {str(e)}")

    def get_thumbnail(self):
        try:
            image_files = [f for f in os.listdir(self.folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if not image_files:
                logger.info("サムネイル画像が見つかりません。")
                return None
            
            return os.path.join(self.folder_path, image_files[0])

        except Exception as e:
            logger.error(f"サムネイル画像の検索中にエラーが発生しました: {str(e)}")
            return None
