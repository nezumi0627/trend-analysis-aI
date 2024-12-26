"""パターン定義パッケージ.

このパッケージは自然言語処理に必要な各種パターンや機能を提供します。

主な機能:
    - 英語/日本語のパターンマッチング (EN_PATTERNS, JP_PATTERNS)
    - ストップワード (EN_STOP_WORDS, JP_STOP_WORDS)
    - 感情分析 (SENTIMENT_PATTERNS, analyze_sentiment)
    - テキスト前処理 (preprocess_text)
    - 文分割 (split_sentences)
    - トークン化 (tokenize_sentence)
"""

from typing import List

from backend.patterns.en_patterns import EN_PATTERNS
from backend.patterns.jp_patterns import JP_PATTERNS
from backend.patterns.sentiment import SENTIMENT_PATTERNS, analyze_sentiment
from backend.patterns.stop_words import EN_STOP_WORDS, JP_STOP_WORDS
from backend.patterns.tokenizer import (
    preprocess_text,
    split_sentences,
    tokenize_sentence,
)

__all__: List[str] = [
    "EN_PATTERNS",
    "JP_PATTERNS",
    "EN_STOP_WORDS",
    "JP_STOP_WORDS",
    "SENTIMENT_PATTERNS",
    "analyze_sentiment",
    "preprocess_text",
    "split_sentences",
    "tokenize_sentence",
]
