"""トレンド分析パッケージ.

このパッケージはトレンド分析に関する機能を提供します。

主な機能:
    - TrendAnalyzer: トレンドの分析を行うクラス
    - ScoringCalculator: スコアの計算を行うクラス
    - TrendScoring: トレンドスコアリングの実装クラス

使用例:
    from backend.services.trend import TrendAnalyzer

    analyzer = TrendAnalyzer()
    result = analyzer.analyze(data)
"""

from backend.services.trend.analyzer import TrendAnalyzer
from backend.services.trend.scoring import ScoringCalculator, TrendScoring

__all__ = ["TrendAnalyzer", "ScoringCalculator", "TrendScoring"]
