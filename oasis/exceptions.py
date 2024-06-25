class OasisError(Exception):
    """OASISパッケージの基本例外"""

class APIError(OasisError):
    """API リクエストが失敗した場合に発生する例外"""

class FileProcessingError(OasisError):
    """ファイル処理中にエラーが発生した場合の例外"""

class ConfigurationError(OasisError):
    """設定エラーが発生した場合の例外"""
