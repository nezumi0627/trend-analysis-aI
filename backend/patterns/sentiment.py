"""感情分析ロジック.

このモジュールはテキストの感情分析を行うための機能を提供します。
"""

import re
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class SentimentPattern:
    """感情パターンを表すデータクラス."""

    word: str
    score: float
    weight: float = 1.0


# 感情分析用の辞書
SENTIMENT_PATTERNS: List[SentimentPattern] = [
    # ポジティブな表現
    SentimentPattern("ポジティブ", 1.2),
    SentimentPattern("最高", 1.5, 1.2),  # 重要度を上げる
    SentimentPattern("素晴らしい", 1.4),
    SentimentPattern("良い", 1.1),
    SentimentPattern("好き", 1.2),
    SentimentPattern("嬉しい", 1.3),
    SentimentPattern("楽しい", 1.3),
    # ネガティブな表現
    SentimentPattern("ネガティブ", 0.7),
    SentimentPattern("悪い", 0.8),
    SentimentPattern("残念", 0.7),
    SentimentPattern("嫌い", 0.7),
    SentimentPattern("つまらない", 0.8),
    SentimentPattern("不満", 0.7),
]


def analyze_sentiment(text: str) -> float:
    """テキストの感情分析を行う.

    Args:
        text (str): 分析対象のテキスト

    Returns:
        float: 感情スコア (1.0が中立、>1.0がポジティブ、<1.0がネガティブ)
    """
    if not text:
        return 1.0

    sentiment_score = 1.0
    word_counts: Dict[str, int] = {}

    # 単語の出現回数をカウント
    for pattern in SENTIMENT_PATTERNS:
        count = len(re.findall(pattern.word, text))
        if count > 0:
            word_counts[pattern.word] = count

    # スコアの計算
    for pattern in SENTIMENT_PATTERNS:
        if pattern.word in word_counts:
            # 出現回数と重みを考慮したスコア計算
            count = word_counts[pattern.word]
            sentiment_score *= pattern.score ** (count * pattern.weight)

    return round(sentiment_score, 3)
