"""トレンドスコアリングパッケージ.

このパッケージはトレンドスコアの計算と評価を行うためのモジュールを提供します。

主な機能:
    - トレンドスコアの計算 (ScoringCalculator)
    - トレンドの評価と分析 (TrendScoring)

Note:
    - スコアリングには時系列データの解析が含まれます
    - 複数の評価指標を組み合わせて総合的なトレンド分析を行います
"""

from backend.services.trend.scoring.calculator import ScoringCalculator
from backend.services.trend.scoring.trend_scoring import TrendScoring

__all__ = [
    "ScoringCalculator",  # トレンドスコア計算クラス
    "TrendScoring",  # トレンド評価・分析クラス
]
