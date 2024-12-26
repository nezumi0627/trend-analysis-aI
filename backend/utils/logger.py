"""ロギング設定.

このモジュールはアプリケーション全体のロギング設定を提供します。
"""

import logging
import logging.handlers
import os
from pathlib import Path
from typing import Optional


def setup_logger(
    log_level: int = logging.INFO,
    log_file: Optional[str] = None,
    max_bytes: int = 10_485_760,  # 10MB
    backup_count: int = 5,
) -> logging.Logger:
    """ロガーを設定し、構成されたロガーインスタンスを返します.

    Args:
        log_level (int): ロギングレベル. デフォルトはINFO
        log_file (Optional[str]): ログファイルのパス. Noneの場合は標準出力のみ
        max_bytes (int): ログファイルの最大サイズ(バイト). デフォルトは10MB
        backup_count (int): 保持するバックアップファイルの数. デフォルトは5

    Returns:
        logging.Logger: 構成されたロガーインスタンス
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    # フォーマッタの設定
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 標準出力へのハンドラを追加
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # ファイルへのログ出力が指定された場合
    if log_file:
        log_dir = Path(log_file).parent
        os.makedirs(log_dir, exist_ok=True)

        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
