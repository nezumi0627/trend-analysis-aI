"""トレンド分析サービス.

テキストからトレンドを抽出・分析し、重要度やスコアを計算するサービス。

主な機能:
    - テキストの言語判定(日本語/英語)
    - 品詞判定と重要度計算
    - 文脈を考慮したトレンド分析
    - トレンドの追跡と更新
"""

import re
from typing import Any, Dict, List, Optional, Tuple

from backend.constants.colors import BLACK, GRAY, POS_COLORS
from backend.constants.english import BE_VERBS, COMMON_VERBS
from backend.constants.japanese import JAPANESE_CHARS
from backend.constants.particles import IMPORTANT_PARTICLES
from backend.constants.patterns import (
    SENTENCE_SEPARATORS,
    TRAILING_SYMBOLS,
)
from backend.patterns.en_patterns import (
    FUNCTION_WORDS,
    INDEPENDENT_WORDS,
)
from backend.patterns.jp_patterns import (
    DEPENDENT_WORDS,
    INDEPENDENT_WORDS as JP_INDEPENDENT_WORDS,
)
from backend.patterns.stop_words import EN_STOP_WORDS, JP_STOP_WORDS


class TrendAnalyzer:
    """トレンド分析クラス."""

    def __init__(self) -> None:
        """初期化."""
        self.jp_stop_words: Dict[str, Any] = JP_STOP_WORDS
        self.en_stop_words: Dict[str, Any] = EN_STOP_WORDS
        # コンパイル済みの正規表現パターンを保持
        self.japanese_chars = re.compile(JAPANESE_CHARS)
        self.sentence_separators = re.compile(SENTENCE_SEPARATORS)
        self.trailing_symbols = re.compile(TRAILING_SYMBOLS)
        self.be_verbs = re.compile(BE_VERBS[0], re.I)
        self.common_verbs = re.compile(COMMON_VERBS, re.I)

    def _is_japanese_text(self, text: str) -> bool:
        """テキストが日本語かどうかを判定する.

        Args:
            text (str): 判定対象のテキスト

        Returns:
            bool: 日本語の場合True
        """
        return bool(self.japanese_chars.search(text))

    def _identify_part_of_speech(self, word: str) -> Tuple[str, float]:
        """単語の品詞と重要度を判定する."""
        return (
            self._identify_japanese_pos(word)
            if self._is_japanese_text(word)
            else self._identify_english_pos(word)
        )

    def _identify_japanese_pos(self, word: str) -> Tuple[str, float]:
        """日本語の品詞と重要度を判定する."""
        # 助詞・助動詞（付属語）
        for pos, patterns in DEPENDENT_WORDS.items():
            for pattern in patterns:
                if re.match(pattern, word):
                    return pos, 0.5

        # 自立語（名詞、動詞、形容詞、副詞）
        for pos, patterns in JP_INDEPENDENT_WORDS.items():
            for pattern in patterns:
                if re.match(pattern, word):
                    return pos, 2.0

        return "記号", 0.1

    def _match_patterns(self, word: str, patterns: List[Any]) -> bool:
        """パターンとのマッチングをチェックする."""
        for pattern in patterns:
            if isinstance(pattern, list):
                if any(re.match(p, word, re.I) for p in pattern):
                    return True
            elif re.match(pattern, word, re.I):
                return True
        return False

    def _identify_english_pos(self, word: str) -> Tuple[str, float]:
        """英語の品詞と重要度を判定する."""
        # 基本動詞
        if self.be_verbs.match(word) or self.common_verbs.match(word):
            return "verb", 2.0

        # 機能語（前置詞、冠詞、代名詞）
        for pos, patterns in FUNCTION_WORDS.items():
            if self._match_patterns(word, patterns):
                return pos, 0.5

        # 自立語（動詞、形容詞、副詞、名詞）
        for pos, patterns in INDEPENDENT_WORDS.items():
            if self._match_patterns(word, patterns):
                return pos, 2.0

        return "symbol", 0.1

    def analyze(self, text: str) -> List[Dict[str, Any]]:
        """テキストを分析し、品詞情報を付与して返す."""
        # 文単位で分割
        sentences = self.sentence_separators.split(text)
        sentences = [s.strip() for s in sentences if s.strip()]

        all_results = []
        for i, sentence in enumerate(sentences):
            # 前後の文脈を取得
            prev_sentence = sentences[i - 1] if i > 0 else None
            next_sentence = (
                sentences[i + 1] if i < len(sentences) - 1 else None
            )

            # 文脈を考慮した分析
            results = self._analyze_with_context(
                sentence, prev_sentence, next_sentence
            )
            all_results.extend(results)

            # 文の区切りを追加
            if i < len(sentences) - 1:
                all_results.append(
                    {
                        "word": "。",
                        "pos": "記号",
                        "importance": 0.1,
                        "color": GRAY,
                    }
                )

        return all_results

    def update_trends(self, db: Any, text: str) -> List[Dict[str, Any]]:
        """トレンドを更新する."""
        from sqlalchemy import select
        from sqlalchemy.sql.expression import text as sql_text

        from backend.models.models import Trend

        trends = []
        words = self._extract_words(text)

        for word in words:
            pos, importance = self._identify_part_of_speech(word)

            # 重要度が低い単語はスキップ
            if importance <= 0.5:
                continue

            # 記号を除去
            word = self.trailing_symbols.sub("", word)
            if not word:
                continue

            # トレンドを更新
            stmt = select(Trend.id, Trend.keyword, Trend.count).where(
                Trend.keyword == word
            )
            result = db.execute(stmt).fetchone()

            if result:
                trend_id = result[0]
                count = result[2] + 1
                db.execute(
                    sql_text(
                        "UPDATE trends SET count = :count WHERE id = :id"
                    ),
                    {"count": count, "id": trend_id},
                )
            else:
                result = db.execute(
                    sql_text(
                        "INSERT INTO trends (keyword, count, created_at) "
                        "VALUES (:keyword, :count, CURRENT_TIMESTAMP) "
                        "RETURNING id, keyword, count"
                    ),
                    {"keyword": word, "count": 1},
                )
                result = result.fetchone()

            if result:
                trends.append(
                    {"id": result[0], "keyword": result[1], "count": result[2]}
                )

            db.commit()

        return trends

    def _analyze_with_context(
        self,
        sentence: str,
        prev_sentence: Optional[str] = None,
        next_sentence: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """文脈を考慮してテキストを分析する."""
        results = []
        words = self._extract_words(sentence)

        # 前後の文脈の単語を取得
        prev_words = (
            self._extract_words(prev_sentence) if prev_sentence else []
        )
        next_words = (
            self._extract_words(next_sentence) if next_sentence else []
        )

        for i, word in enumerate(words):
            # 基本の品詞と重要度を取得
            pos, importance = self._identify_part_of_speech(word)

            # 文脈に基づいて重要度を調整
            importance = self._adjust_importance(
                word,
                pos,
                importance,
                words,
                i,  # 現在の文の情報
                prev_words,
                next_words,  # 前後の文の情報
            )

            color = self._get_color_for_pos(pos, importance)
            results.append(
                {
                    "word": word,
                    "pos": pos,
                    "importance": importance,
                    "color": color,
                }
            )

        return results

    def _extract_words(self, text: str) -> List[str]:
        """テキストから単語を抽出する."""
        if not text:
            return []

        words = []
        current_word = ""

        for char in text:
            if char.isspace():
                if current_word:
                    words.append(current_word)
                    current_word = ""
                continue

            # 日本語の場合
            if self._is_japanese_text(char):
                if current_word:
                    words.append(current_word)
                current_word = char
            # 英語の場合
            else:
                if self._is_japanese_text(current_word):
                    if current_word:
                        words.append(current_word)
                    current_word = char
                else:
                    current_word += char

        if current_word:
            words.append(current_word)

        return words

    def _adjust_importance(
        self,
        word: str,
        pos: str,
        base_importance: float,
        current_words: List[str],
        current_index: int,
        prev_words: List[str],
        next_words: List[str],
    ) -> float:
        """文脈に基づいて重要度を調整する."""
        importance = base_importance
        importance = self._adjust_by_position(
            importance, current_index, len(current_words)
        )
        importance = self._adjust_by_context(
            importance, word, prev_words, next_words
        )
        importance = self._adjust_by_grammar(
            importance, word, pos, current_words, current_index
        )
        return min(importance, 3.0)

    def _adjust_by_position(
        self, importance: float, index: int, length: int
    ) -> float:
        """位置に基づく重要度の調整."""
        return (
            importance * 1.2
            if index == 0 or index == length - 1
            else importance
        )

    def _adjust_by_context(
        self,
        importance: float,
        word: str,
        prev_words: List[str],
        next_words: List[str],
    ) -> float:
        """前後の文脈に基づいて重要度を調整する."""
        return (
            importance * 1.5
            if word in prev_words or word in next_words
            else importance
        )

    def _adjust_by_grammar(
        self,
        importance: float,
        word: str,
        pos: str,
        words: List[str],
        index: int,
    ) -> float:
        """文法的な特徴に基づく重要度の調整."""
        if self._is_japanese_text(word):
            if (
                pos == "名詞"
                and index < len(words) - 1
                and words[index + 1] in IMPORTANT_PARTICLES
            ):
                importance *= 1.3
            elif pos == "動詞" and index == len(words) - 1:
                importance *= 1.2
        else:
            if (
                pos == "noun"
                and index > 0
                and self._identify_part_of_speech(words[index - 1])[0]
                in ["article", "adjective"]
            ):
                importance *= 1.3
            elif (
                pos == "verb"
                and index > 0
                and self._identify_part_of_speech(words[index - 1])[0]
                in ["noun", "pronoun"]
            ):
                importance *= 1.2
        return importance

    def _get_color_for_pos(self, pos: str, importance: float) -> str:
        """品詞に応じた表示色を返す."""
        if importance <= 0.5:
            return GRAY  # グレー（低重要度）

        return POS_COLORS.get(pos, BLACK)  # デフォルトは黒

    def get_patterns(self) -> Dict[str, Dict[str, Any]]:
        """パターン情報を取得する."""

        def convert_patterns(patterns: Dict[str, Any]) -> Dict[str, Any]:
            result = {}
            for key, value in patterns.items():
                if isinstance(value, list):
                    result[key] = [str(p) for p in value]
                else:
                    result[key] = str(value)
            return result

        return {
            "jp": {
                **convert_patterns(JP_INDEPENDENT_WORDS),
                **convert_patterns(DEPENDENT_WORDS),
            },
            "en": {
                **convert_patterns(INDEPENDENT_WORDS),
                **convert_patterns(FUNCTION_WORDS),
            },
        }
