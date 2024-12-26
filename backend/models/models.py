"""データモデル定義.

SQLAlchemyを使用したデータベースモデルを定義するモジュール。
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, Index, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """ベースモデル.

    全てのモデルクラスの基底クラス。
    """

    pass


class Trend(Base):
    """トレンドモデル.

    トレンドキーワードとその関連データを格納するモデル。

    Attributes:
        id (int): プライマリーキー
        keyword (str): トレンドキーワード
        count (int): キーワードの出現回数
        score (float, optional): キーワードのスコア値
        created_at (datetime): レコード作成日時
        updated_at (datetime): レコード更新日時
    """

    __tablename__ = "trends"
    __table_args__ = (
        Index("ix_trends_keyword", "keyword"),
        Index("ix_trends_created_at", "created_at"),
    )

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    keyword: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )
    count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
