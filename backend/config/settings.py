"""アプリケーション設定.

このモジュールはアプリケーション全体の設定を管理します。

設定項目:
    - ベースディレクトリ設定
    - データベース接続設定
    - フロントエンド関連パス設定
"""

from pathlib import Path
from typing import Any, Dict

# ベースディレクトリ
BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

# データベース設定
SQLALCHEMY_DATABASE_URL: str = "sqlite:///./trends.db"
DB_CONNECT_ARGS: Dict[str, Any] = {
    "check_same_thread": False,
    "timeout": 30,  # 接続タイムアウト(秒)
    "isolation_level": "DEFERRED",  # トランザクション分離レベル
}

# フロントエンド設定
TEMPLATE_DIR: Path = BASE_DIR / "frontend" / "templates"
STATIC_DIR: Path = BASE_DIR / "frontend" / "static"

# セキュリティ設定
SECRET_KEY: str = "your-secret-key-here"  # 本番環境では環境変数から取得すべき
ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"]

# ロギング設定
LOG_DIR: Path = BASE_DIR / "logs"
LOG_LEVEL: str = "INFO"
