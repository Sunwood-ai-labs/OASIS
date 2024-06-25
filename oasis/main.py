from .oasis import OASIS
from .logger import logger

def process_folder(folder_path: str):
    try:
        oasis = OASIS()
        result = oasis.process_folder(folder_path)
        return result
    except Exception as e:
        logger.error(f"フォルダ処理中にエラーが発生しました: {str(e)}")
        raise
