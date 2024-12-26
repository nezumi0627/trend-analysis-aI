"""トレンドスコアリングロジック.

トレンドの重要度とスコアを計算し、人気順・最新順でトレンドを取得する機能を提供する。
"""

from datetime import datetime, timedelta
from typing import Dict, List, Union

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.models import Trend
from backend.patterns.en_patterns import EN_PATTERNS
from backend.patterns.jp_patterns import JP_PATTERNS
from backend.services.trend.scoring.calculator import ScoringCalculator


class TrendScoring:
    """トレンドのスコアリングを管理するクラス.

    トレンドの重要度を計算し、時系列データに基づいて人気スコアを算出する。
    また、様々な条件でトレンドを取得する機能を提供する。

    Attributes:
        jp_patterns: 日本語のパターンマッチング用辞書
        en_patterns: 英語のパターンマッチング用辞書
        importance_weights: 各要素の重要度の重み付け
        trend_indicators: トレンド性を評価するためのキーワード
        calculator: スコア計算を行うCalculatorインスタンス
    """

    def __init__(self):
        """初期化."""
        self.jp_patterns = JP_PATTERNS
        self.en_patterns = EN_PATTERNS

        # 重要度の重み付け
        self.importance_weights: Dict[str, float] = {
            "名詞": 1.0,
            "複合名詞": 1.3,
            "造語": 1.5,
            "ハッシュタグ": 1.4,
            "noun": 1.0,
            "compound": 1.3,
            "neologism": 1.5,
            "hashtag": 1.4,
        }

        # トレンド性の評価用パターン
        self.trend_indicators: set[str] = {
            "話題",
            "注目",
            "人気",
            "流行",
            "急上昇",
            "最新",
            "新機能",
            "trend",
            "viral",
            "popular",
            "new",
            "breaking",
            "latest",
            "hot",
            "buzz",
            "trending",
        }

        # スコア計算機の初期化
        self.calculator = ScoringCalculator(
            self.importance_weights, self.trend_indicators
        )

    def calculate_popularity_score(
        self, count: int, hours_old: float, keyword: str
    ) -> float:
        """人気スコアを計算する.

        Args:
            count (int): キーワードの出現回数
            hours_old (float): キーワードの経過時間（時間）
            keyword (str): 評価対象のキーワード

        Returns:
            float: 計算された人気スコア
        """
        return self.calculator.calculate_popularity_score(
            count, hours_old, keyword, self.jp_patterns, self.en_patterns
        )

    def get_top_trends(
        self, db: Session, limit: int = 10
    ) -> List[Dict[str, Union[str, int, float]]]:
        """人気順にトレンドを取得する.

        Args:
            db (Session): データベースセッション
            limit (int, optional): 取得する件数. デフォルトは10

        Returns:
            List[Dict[str, Union[str, int, float]]]: トレンド情報のリスト
        """
        now = datetime.now()
        cutoff_time = now - timedelta(hours=24)

        # 高スコアと新しさを考慮したクエリ
        trends = list(
            db.scalars(
                select(Trend)
                .where(Trend.created_at >= cutoff_time)
                .order_by(
                    Trend.score.desc(),
                    Trend.count.desc(),
                    Trend.created_at.desc(),
                )
                .limit(limit)
            ).all()
        )

        return self._format_trends(db, trends)

    def get_latest_trends(
        self, db: Session, limit: int = 10
    ) -> List[Dict[str, Union[str, int, float]]]:
        """最新順にトレンドを取得する.

        直近6時間のトレンドを優先的に取得し、残りは24時間以内の
        重要なトレンドから補完する。

        Args:
            db (Session): データベースセッション
            limit (int, optional): 取得する件数. デフォルトは10

        Returns:
            List[Dict[str, Union[str, int, float]]]: トレンド情報のリスト
        """
        now = datetime.now()
        cutoff_time = now - timedelta(hours=24)

        # 直近6時間のトレンドを優先
        recent_cutoff = now - timedelta(hours=6)
        recent_trends = db.scalars(
            select(Trend)
            .where(Trend.created_at >= recent_cutoff)
            .order_by(Trend.created_at.desc())
            .limit(limit // 2)
        ).all()

        # 残りは24時間以内の重要なトレンド
        remaining_limit = limit - len(recent_trends)
        if remaining_limit > 0:
            remaining_trends = db.scalars(
                select(Trend)
                .where(
                    Trend.created_at >= cutoff_time,
                    Trend.created_at < recent_cutoff,
                    Trend.count > 100,  # 重要なものだけ
                    Trend.score > 0.5,  # スコアによるフィルタリングを追加
                )
                .order_by(Trend.score.desc(), Trend.created_at.desc())
                .limit(remaining_limit)
            ).all()
        else:
            remaining_trends = []

        all_trends = list(recent_trends) + list(remaining_trends)
        return self._format_trends(db, all_trends)

    def _format_trends(
        self, db: Session, trends: List[Trend]
    ) -> List[Dict[str, Union[str, int, float]]]:
        """トレンドデータをフォーマット.

        Args:
            db (Session): データベースセッション
            trends (List[Trend]): フォーマット対象のトレンドリスト

        Returns:
            List[Dict[str, Union[str, int, float]]]: フォーマット済みトレンド
        """
        return [
            {
                "keyword": str(trend.keyword),
                "count": int(
                    db.scalar(select(func.coalesce(trend.count, 0))) or 0
                ),
                "score": round(
                    float(
                        db.scalar(select(func.coalesce(trend.score, 0.0)))
                        or 0.0
                    ),
                    2,
                ),
                "created_at": trend.created_at.isoformat(),
                "trend_type": self._determine_trend_type(trend),
            }
            for trend in trends
        ]

    def _determine_trend_type(self, trend: Trend) -> str:
        """トレンドの種類を判定する.

        Args:
            trend (Trend): 判定対象のトレンド

        Returns:
            str: トレンドの種類（"hot", "rising", "new"のいずれか）
        """
        hours_old = (datetime.now() - trend.created_at).total_seconds() / 3600

        if (
            trend.score is not None
            and trend.score > 0.8
            and trend.count > 1000
        ):
            return "hot"
        if trend.score is not None and trend.score > 0.5 and hours_old < 6:
            return "rising"
        return "new"
