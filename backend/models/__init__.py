"""モデルパッケージ.

このパッケージはデータベースモデルの定義を含みます。

主なモデル:
    - Base: 全モデルの基底クラス
    - Trend: トレンドデータを表現するモデル

Note:
    全てのモデルはSQLAlchemyのDeclarativeBaseを継承しています。
"""

from backend.models.models import Base, Trend

__all__ = ["Base", "Trend"]
