"""スコア計算モジュール."""

import re
from typing import Dict, Pattern, Set


class ScoringCalculator:
    """スコア計算を管理するクラス.

    キーワードの人気度、時間経過、重要度、トレンド性を考慮して総合的なスコアを算出する。
    """

    def __init__(
        self, importance_weights: Dict[str, float], trend_indicators: Set[str]
    ):
        """初期化.

        Args:
            importance_weights (Dict[str, float]):
                キーワードパターンごとの重要度の重み
            trend_indicators (Set[str]):
                トレンド指標のキーワードセット
        """
        self.importance_weights = importance_weights
        self.trend_indicators = trend_indicators
        self._compile_regex_cache: Dict[str, Pattern] = {}

    def calculate_popularity_score(
        self,
        count: int,
        hours_old: float,
        keyword: str,
        jp_patterns: Dict[str, list],
        en_patterns: Dict[str, list],
    ) -> float:
        """人気スコアを計算する.

        Args:
            count (int): キーワードの出現回数
            hours_old (float): キーワードが最初に出現してからの経過時間
                （時間単位）
            keyword (str): 評価対象のキーワード
            jp_patterns (Dict[str, list]): 日本語のパターン辞書
            en_patterns (Dict[str, list]): 英語のパターン辞書

        Returns:
            float: 計算された最終スコア（小数点2桁で丸められる）
        """
        if not keyword or hours_old < 0:
            return 0.0

        # 基本スコア（出現回数に基づく対数的なスケーリング）
        base_score = count * 10 * (1 + 0.1 * len(str(count)))

        # 時間減衰（より細かい時間帯で重み付け）
        time_weight = self._calculate_time_weight(hours_old)

        # キーワードの重要度を計算（キャッシュ付き）
        importance_weight = self._calculate_keyword_importance(
            keyword, jp_patterns, en_patterns
        )

        # トレンド性の評価（拡張版）
        trend_bonus = self._evaluate_trend_indicators(keyword)

        # 最終スコアの計算（正規化付き）
        raw_score = (
            base_score * time_weight * importance_weight * (1 + trend_bonus)
        )
        normalized_score = min(raw_score, 10000)  # スコアの上限設定

        return round(normalized_score, 2)

    def _calculate_time_weight(self, hours_old: float) -> float:
        """時間重みを計算.

        Args:
            hours_old (float): 経過時間（時間単位）

        Returns:
            float: 計算された時間重み
        """
        if hours_old <= 0.5:
            return 1.5  # 30分以内
        if hours_old <= 1:
            return 1.2  # 1時間以内
        if hours_old <= 3:
            return 1.0  # 3時間以内
        if hours_old <= 6:
            return 0.9  # 6時間以内
        if hours_old <= 12:
            return 0.7  # 12時間以内
        if hours_old <= 24:
            return 0.5  # 24時間以内
        return 0.3  # 24時間超過

    def _calculate_keyword_importance(
        self,
        keyword: str,
        jp_patterns: Dict[str, list],
        en_patterns: Dict[str, list],
    ) -> float:
        """キーワードの重要度を計算.

        Args:
            keyword (str): 評価対象のキーワード
            jp_patterns (Dict[str, list]): 日本語のパターン辞書
            en_patterns (Dict[str, list]): 英語のパターン辞書

        Returns:
            float: 計算された重要度の重み
        """
        max_weight = 1.0
        keyword = keyword.lower()

        def check_patterns(patterns_dict: Dict[str, list]) -> None:
            nonlocal max_weight
            for pattern_type, patterns in patterns_dict.items():
                for pattern in patterns:
                    if pattern not in self._compile_regex_cache:
                        self._compile_regex_cache[pattern] = re.compile(
                            pattern, re.I
                        )
                    if self._compile_regex_cache[pattern].search(keyword):
                        weight = self.importance_weights[pattern_type]
                        max_weight = max(max_weight, weight)

        check_patterns(jp_patterns)
        check_patterns(en_patterns)

        return max_weight

    def _evaluate_trend_indicators(self, keyword: str) -> float:
        """トレンド性を評価.

        Args:
            keyword (str): 評価対象のキーワード

        Returns:
            float: 計算されたトレンドボーナス（0.0-1.0の範囲）
        """
        bonus = 0.0
        keyword_lower = keyword.lower()

        # トレンド指標との一致をチェック（部分一致も考慮）
        for indicator in self.trend_indicators:
            if indicator in keyword_lower:
                bonus += 0.2
            elif any(part in keyword_lower for part in indicator.split()):
                bonus += 0.1

        # 特殊な形式のボーナス（拡張）
        if "#" in keyword:
            bonus += 0.3
        if "@" in keyword:  # メンション
            bonus += 0.2
        if re.search(r"\d+", keyword):  # 数字を含む
            bonus += 0.1
        if len(keyword) <= 10:  # 短いキーワード
            bonus += 0.1
        if re.search(r"[!?！？]+", keyword):  # 感嘆符や疑問符
            bonus += 0.15
        if re.search(r"(速報|breaking|urgent)", keyword_lower):  # 緊急性
            bonus += 0.25

        return min(bonus, 1.0)  # 最大1.0までの制限
