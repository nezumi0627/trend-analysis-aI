"""データベース接続と操作の管理.

SQLAlchemyを使用したデータベース操作の基本機能を提供するモジュール.
"""

import logging
from contextlib import contextmanager
from typing import Generator, Optional

from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from backend.config.settings import DB_CONNECT_ARGS, SQLALCHEMY_DATABASE_URL
from backend.models.models import Base

logger = logging.getLogger(__name__)


class DatabaseManager:
    """データベース接続とセッション管理を行うクラス."""

    _instance: Optional["DatabaseManager"] = None
    _engine: Optional[Engine] = None

    def __new__(cls) -> "DatabaseManager":
        """インスタンスを生成する."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """データベースエンジンとセッションファクトリを初期化."""
        if self._engine is None:
            self._engine = create_engine(
                SQLALCHEMY_DATABASE_URL,
                connect_args=DB_CONNECT_ARGS,
                pool_pre_ping=True,
            )
            self.SessionLocal = sessionmaker(
                autocommit=False, autoflush=False, bind=self._engine
            )
            # 起動時にテーブルを作成
            Base.metadata.create_all(bind=self._engine)
            logger.info("Database engine initialized successfully")


db_manager = DatabaseManager()


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """データベースセッションを取得する.

    コンテキストマネージャとして使用することで、セッションの自動クローズを保証する.

    Yields:
        Session: データベースセッション

    Raises:
        SQLAlchemyError: データベース操作でエラーが発生した場合
    """
    db = db_manager.SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error occurred: {str(e)}")
        raise
    finally:
        db.close()


def init_db() -> None:
    """データベースを初期化する.

    既存のテーブルを全て削除し、新しくテーブルを作成する.

    Raises:
        SQLAlchemyError: データベース初期化でエラーが発生した場合
    """
    try:
        if db_manager._engine is not None:
            Base.metadata.drop_all(bind=db_manager._engine)
            Base.metadata.create_all(bind=db_manager._engine)
            logger.info("Database initialized successfully")
    except SQLAlchemyError as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise


def close_db() -> None:
    """データベース接続を安全に閉じる.

    全てのコネクションプールをクリーンアップし、エンジンを破棄する.
    """
    if db_manager._engine:
        db_manager._engine.dispose()
        logger.info("Database connections closed successfully")
