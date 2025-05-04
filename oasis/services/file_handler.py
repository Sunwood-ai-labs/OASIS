import os
from datetime import datetime
from ..logger import logger
from ..exceptions import FileProcessingError

class FileHandler:
    def __init__(self, folder_path=None):
        self.folder_path = folder_path
        
    def create_dated_folder(self, markdown_file, image_file=None):
        """日付付きのフォルダを作成し、ファイルを移動する"""
        try:
            # タイムスタンプでフォルダ名を生成
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            folder_path = os.path.join(os.path.dirname(markdown_file), timestamp)
            
            # フォルダが存在しない場合は作成
            os.makedirs(folder_path, exist_ok=True)
            
            # マークダウンファイルを移動
            new_md_path = os.path.join(folder_path, os.path.basename(markdown_file))
            os.makedirs(folder_path, exist_ok=True)
            os.rename(markdown_file, new_md_path)
            
            # 画像ファイルが指定されている場合は移動
            if image_file and os.path.exists(image_file):
                new_img_path = os.path.join(folder_path, os.path.basename(image_file))
                os.rename(image_file, new_img_path)
            
            # フォルダパスを更新
            self.folder_path = folder_path
            logger.info(f"フォルダを作成しました: {folder_path}")
            return folder_path
            
        except Exception as e:
            logger.error(f"フォルダの作成中にエラーが発生しました: {str(e)}")
            raise FileProcessingError(f"フォルダの作成に失敗しました: {str(e)}")
    
    def _sanitize_filename(self, filename):
        """ファイル名に使用できない文字を置換"""
        # スペースをアンダースコアに置換
        filename = filename.replace(' ', '_')
        # 使用できない文字を削除または置換
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '')
        return filename.lower()

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
            
            # タイトル行を除いたコンテンツ（他の見出しは保持）
            content = '\n'.join(lines[lines.index(next(line for line in lines if line.startswith('#')))+1:])

            return content.strip(), title

        except Exception as e:
            logger.error(f"Markdownファイルの読み込み中にエラーが発生しました: {str(e)}")
            raise FileProcessingError(f"Markdownファイルの読み込みに失敗しました: {str(e)}")

    def get_thumbnail(self):
        try:
            if not self.folder_path:
                logger.info("フォルダパスが設定されていません。")
                return None
                
            image_files = [f for f in os.listdir(self.folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if not image_files:
                logger.info("サムネイル画像が見つかりません。")
                return None
            
            return os.path.join(self.folder_path, image_files[0])

        except Exception as e:
            logger.error(f"サムネイル画像の検索中にエラーが発生しました: {str(e)}")
            return None
