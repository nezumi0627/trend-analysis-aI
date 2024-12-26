"""設定パッケージ.

このパッケージは、アプリケーションの設定に関連する定数や設定値を管理します。

主な設定:
    - STATIC_DIR: 静的ファイルのディレクトリパス
    - TEMPLATE_DIR: テンプレートファイルのディレクトリパス

Note:
    設定値の変更は慎重に行ってください。
"""

from backend.config.settings import (
    STATIC_DIR,
    TEMPLATE_DIR,
)

__all__ = [
    "STATIC_DIR",
    "TEMPLATE_DIR",
]
