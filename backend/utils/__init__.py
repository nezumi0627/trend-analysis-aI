"""ユーティリティパッケージ.

このパッケージはアプリケーション全体で使用される共通のユーティリティ機能を提供します。

主な機能:
    - setup_logger: アプリケーションのロギング設定を行う関数

使用例:
    from backend.utils import setup_logger

    logger = setup_logger(__name__)
    logger.info("アプリケーションを開始します")
"""

from backend.utils.logger import setup_logger

__all__ = ["setup_logger"]
