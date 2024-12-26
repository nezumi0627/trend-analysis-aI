"""テキスト分割ロジック.

このモジュールは、テキストを文や単語に分割するための機能を提供します。
日本語と英語の両方に対応し、形態素解析に基づいて適切な分割を行います。
また、文脈を考慮した高度な分割処理や、特殊なケースへの対応も行います。
"""

import re
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Pattern, Set, Tuple

from backend.constants.english import (
    ARTICLES,
    BE_VERBS,
    COMMON_VERBS,
    COMPOUND_WORDS,
    PREPOSITIONS,
    PRONOUNS,
    TECH_WORDS,
)
from backend.constants.japanese import (
    AUXILIARY_VERBS,
    BASIC_PARTICLES,
    COMPOUND_PARTICLES,
    JAPANESE_CHARS,
    VERB_CONJUGATION,
    VERB_STEM_ENDINGS,
)
from backend.patterns.en_patterns import (
    INDEPENDENT_WORDS,
    SYMBOLS as EN_SYMBOLS,
)
from backend.patterns.jp_patterns import (
    DEPENDENT_WORDS,
    INDEPENDENT_WORDS as JP_INDEPENDENT_WORDS,
    SPECIAL,
    SYMBOLS as JP_SYMBOLS,
)


class Language(Enum):
    """言語種別を���挙型."""

    JAPANESE = auto()
    ENGLISH = auto()
    UNKNOWN = auto()  # 言語判定できない場合用


@dataclass
class Token:
    """分割された単語を表すデータクラス.

    Attributes:
        text (str): トークンのテキスト
        pos (str): 品詞情報
        language (Language): 言語種別
        is_compound (bool): 複合語かどうか
        original_form (str): 原形（活用語の場合）
        features (Dict[str, str]): その他の特徴情報
    """

    text: str
    pos: str
    language: Language
    is_compound: bool = False
    original_form: Optional[str] = None
    features: Dict[str, str] = field(default_factory=dict)


def preprocess_text(text: str) -> str:
    """テキストの前処理を行う.

    Args:
        text (str): 前処理対象のテキスト

    Returns:
        str: 前処理済みのテキスト

    Note:
        - 文字の正規化
        - 不要な空白の除去
        - 制御文字の除去
        - 全角文字の半角変換
        を行います。
    """
    if not text:
        return ""

    # 改行と余分な空白の処理
    text = re.sub(r"\s+", " ", text.strip())

    # 全角英数字を半角に変換
    text = text.translate(
        str.maketrans(
            "０１２３４５６７８９ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ",
            "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        )
    )

    # 全角記号を半角に変換（文字数を一致させる）
    text = text.translate(
        str.maketrans("：；？！（）［］｛｝＜＞、，", ":;?!()[]{}<>,,")
    )

    # 制御文字を除去
    text = re.sub(r"[\x00-\x1F\x7F-\x9F]", "", text)

    # 重複する句読点を単一に
    text = re.sub(r"[。．.]{2,}", "。", text)
    text = re.sub(r"[、，,]{2,}", "、", text)

    return text.strip()


def split_sentences(text: str) -> List[str]:
    """テキストを文単位に分割する.

    Args:
        text (str): 分割対象のテキスト

    Returns:
        List[str]: 分割された文のリスト

    Note:
        - 引用符や括弧の対応を考慮
        - 箇条書きや番号付きリストに対応
        - 省略記号(...)を考慮
    """
    # より正確な文分割パターン
    pattern = (
        r"(?<!\.\.)(?<!Mr)(?<!Mrs)(?<!Dr)(?<!Jr)(?<!Sr)(?<!Ltd)(?<!Inc)"
        # 略語の除外
        r"[。！？!?．.]+[\s]*"
        # 句読点の後に空白を挿入
        r"(?=(?:[^「」『』（）\(\)]*$|[「」『』（）\(\)][^「」『』（）\(\)]*$))"
        # 括弧の対応を考慮
    )

    # 箇条書きや番号付きリストを考慮した分割
    list_pattern = r"(?:^|\n)(?:\d+[\.)］】]|\-|\*|\・|\○|\◎|\●)\s*"

    # 文の分割
    raw_sentences = re.split(pattern, text)
    sentences = []
    current = ""

    for s in raw_sentences:
        # リスト項目の処理
        list_items = re.split(list_pattern, s)
        if len(list_items) > 1:
            for item in list_items:
                if item.strip():
                    current += item
                    if _is_balanced(current):
                        sentences.append(current.strip())
                        current = ""
        else:
            current += s
            if _is_balanced(current):
                sentences.append(current.strip())
                current = ""

    if current:
        sentences.append(current.strip())

    return [s for s in sentences if s]


def _is_balanced(text: str) -> bool:
    """括弧や引用符が正しく対応しているか確認する.

    Args:
        text (str): チェック対象のテキスト

    Returns:
        bool: 括弧や引用符が正しく対応している場合True
    """
    pairs = {
        "「": "」",
        "『": "』",
        "(": ")",
        "（": "）",
        "[": "]",
        "［": "］",
        "{": "}",
        "｛": "｝",
        "＜": "＞",
        "<": ">",
    }
    stack = []
    escaped = False

    for i, char in enumerate(text):
        if char == "\\":
            escaped = True
            continue

        if escaped:
            escaped = False
            continue

        if char in pairs:
            stack.append((char, i))
        elif char in pairs.values():
            if not stack:
                return False
            last_char, _ = stack.pop()
            if pairs[last_char] != char:
                return False

    return len(stack) == 0


def tokenize_sentence(sentence: str) -> List[Token]:
    """文を単語に分割する.

    Args:
        sentence (str): 分割対象の文

    Returns:
        List[Token]: 分割された単語のリスト（品詞情報付き）
    """
    tokens: List[Token] = []
    current_word = ""
    current_type = None  # 現在の文字種類（日本語/英語/その他）

    for char in sentence:
        # カンマやピリオドの処理
        if char in ["、", "，", ",", "。", "．", "."]:
            if current_word:
                tokens.append(_create_token(current_word))
                current_word = ""
            current_type = None
            continue

        # 空白の処理
        if char.isspace():
            if current_word:
                tokens.append(_create_token(current_word))
                current_word = ""
            current_type = None
            continue

        # 文字種の判定
        if re.match(JAPANESE_CHARS, char):
            char_type = "jp"
        elif char.isascii():
            char_type = "en"
        else:
            char_type = "other"

        # 文字種が変わった場合、または日本語の場合は文字ごとに分割
        if current_type != char_type or char_type == "jp":
            if current_word:
                tokens.append(_create_token(current_word))
                current_word = ""
            current_type = char_type

        current_word += char

    # 残りの文字の処理
    if current_word:
        tokens.append(_create_token(current_word))

    return tokens


def _create_token(text: str) -> Token:
    """トークンを生成する.

    Args:
        text (str): トークンのテキスト

    Returns:
        Token: 生成されたトークン
    """
    # 言語判定
    if re.search(JAPANESE_CHARS, text):
        lang = Language.JAPANESE
        # 日本語の品詞判定
        if re.match(r"[はがをのにへとでもや]", text):
            pos = "助詞"
        elif re.match(r"[あ-ん]+", text):
            pos = "動詞"  # 簡易的な判定
        else:
            pos = "名詞"  # デフォルト
    elif text.isascii():
        lang = Language.ENGLISH
        # 英語の品詞判定（簡易）
        if text.lower() in {"a", "an", "the"}:
            pos = "article"
        elif text.isalpha():
            pos = "word"
        else:
            pos = "symbol"
    else:
        lang = Language.UNKNOWN
        pos = "unknown"

    return Token(
        text=text,
        pos=pos,
        language=lang,
        is_compound=False,
        original_form=None,
        features={},
    )


def _detect_language(text: str) -> Language:
    """テキストの言語を判定する.

    Args:
        text (str): 判定対象のテキスト

    Returns:
        Language: 判定された言語
    """
    # 日本語文字の検出
    jp_ratio = len(re.findall(JAPANESE_CHARS, text)) / len(text) if text else 0

    # 英語文字の検出
    en_ratio = len(re.findall(r"[a-zA-Z]", text)) / len(text) if text else 0

    if jp_ratio > 0.3:
        return Language.JAPANESE
    if en_ratio > 0.3:
        return Language.ENGLISH
    return Language.UNKNOWN


def _check_compound_word(
    text: str, lang: Language, seen_compounds: Set[str]
) -> Optional[Tuple[Token, int]]:
    """複合語をチェックする.

    Args:
        text (str): チェック対象のテキスト
        lang (Language): 言語種別
        seen_compounds (Set[str]): 既出の複合語

    Returns:
        Optional[Tuple[Token, int]]: 複合語トークンと長さのペア
    """
    if lang == Language.JAPANESE:
        compounds = [w for w in COMPOUND_WORDS if w not in seen_compounds]
        for compound in compounds:
            if text.startswith(compound):
                seen_compounds.add(compound)
                return Token(
                    compound, "複合語", Language.JAPANESE, is_compound=True
                ), len(compound)
    else:
        compounds = [w for w in TECH_WORDS if w not in seen_compounds]
        for compound in compounds:
            if text.lower().startswith(compound.lower()):
                seen_compounds.add(compound)
                return Token(
                    compound, "compound", Language.ENGLISH, is_compound=True
                ), len(compound)

    return None


def _build_jp_patterns() -> List[Tuple[Pattern, str]]:
    """日本語のパターンを構築する.

    Returns:
        List[Tuple[Pattern, str]]: パターンと品詞のペアのリスト
    """
    patterns = []

    # 助動詞（最も長いパターンを先に）
    patterns.extend(
        [(re.compile(rf"\b{p}\b"), "助動詞") for p in AUXILIARY_VERBS]
    )
    patterns.extend(
        [
            (re.compile(rf"\b{p}\b"), "助動詞")
            for p in DEPENDENT_WORDS["助動詞"]
        ]
    )

    # 助詞（複合助詞を先に）
    patterns.extend(
        [(re.compile(rf"\b{p}\b"), "助詞") for p in COMPOUND_PARTICLES]
    )
    patterns.extend(
        [(re.compile(rf"\b{p}\b"), "助詞") for p in DEPENDENT_WORDS["助詞"]]
    )

    # 動詞（活用形を含む）
    verb_pattern = (
        rf"{JAPANESE_CHARS}+(?:{VERB_STEM_ENDINGS}|{VERB_CONJUGATION})\b"
    )
    patterns.append((re.compile(verb_pattern), "動詞"))
    patterns.extend(
        [
            (re.compile(rf"\b{p}\b"), "動詞")
            for p in JP_INDEPENDENT_WORDS["動詞"]
        ]
    )

    # その他の自立語
    for pos in ["形容詞", "副詞", "名詞"]:
        patterns.extend(
            [(re.compile(rf"\b{p}\b"), pos) for p in JP_INDEPENDENT_WORDS[pos]]
        )

    # 特殊な語
    for pos in ["接続詞", "感動詞"]:
        patterns.extend([(re.compile(rf"\b{p}\b"), pos) for p in SPECIAL[pos]])

    # 記号
    patterns.extend(
        [(re.compile(re.escape(p)), "記号") for p in JP_SYMBOLS["記号"]]
    )

    return patterns


def _build_en_patterns() -> List[Tuple[Pattern, str]]:
    """英語のパターンを構築する.

    Returns:
        List[Tuple[Pattern, str]]: パターンと品詞のペアのリスト
    """
    patterns = []

    # 基本動詞
    patterns.extend(
        [(re.compile(rf"\b{p}\b", re.IGNORECASE), "verb") for p in BE_VERBS]
    )
    patterns.extend(
        [
            (re.compile(rf"\b{p}\b", re.IGNORECASE), "verb")
            for p in COMMON_VERBS
        ]
    )

    # 機能語
    patterns.extend(
        [
            (re.compile(rf"\b{p}\b", re.IGNORECASE), "preposition")
            for p in PREPOSITIONS
        ]
    )
    patterns.extend(
        [(re.compile(rf"\b{p}\b", re.IGNORECASE), "article") for p in ARTICLES]
    )
    patterns.extend(
        [(re.compile(rf"\b{p}\b", re.IGNORECASE), "pronoun") for p in PRONOUNS]
    )

    # 自立語
    for pos in ["verb", "adjective", "adverb", "noun"]:
        patterns.extend(
            [
                (re.compile(rf"\b{p}\b", re.IGNORECASE), pos)
                for p in INDEPENDENT_WORDS[pos]
            ]
        )

    # 複合語
    patterns.extend(
        [
            (re.compile(rf"\b{p}\b", re.IGNORECASE), "compound")
            for p in COMPOUND_WORDS
        ]
    )
    patterns.extend(
        [(re.compile(rf"\b{p}\b", re.IGNORECASE), "tech") for p in TECH_WORDS]
    )

    # 記号
    patterns.extend(
        [
            (re.compile(re.escape(p)), "punctuation")
            for p in EN_SYMBOLS["punctuation"]
        ]
    )

    return patterns


def _find_longest_match(
    text: str, patterns: List[Tuple[Pattern, str]], lang: Language
) -> Optional[Tuple[Token, int]]:
    """最長一致でマッチするパターンを探す.

    Args:
        text (str): 検索対象のテキスト
        patterns (List[Tuple[Pattern, str]]): パターンと品詞のペアのリスト
        lang (Language): 言語種別

    Returns:
        Optional[Tuple[Token, int]]: マッチしたトークンと長さのペア
    """
    longest_match = None
    longest_length = 0
    matched_pos = ""
    matched_features: Dict[str, str] = {}

    for pattern, pos in patterns:
        match = pattern.match(text)
        if match:
            word = match.group(0).strip()
            if word and len(word) > longest_length:
                longest_match = word
                longest_length = len(word)
                matched_pos = pos

                # 追加の特徴抽出
                if lang == Language.JAPANESE:
                    matched_features = _extract_jp_features(word, pos)
                else:
                    matched_features = _extract_en_features(word, pos)

    if longest_match:
        return Token(
            longest_match, matched_pos, lang, features=matched_features
        ), longest_length

    return None


def _handle_unknown_token(text: str) -> Token:
    """未知のトークンを処理する.

    Args:
        text (str): 処理対象のテキスト

    Returns:
        Token: 生成されたトークン
    """
    # 英単語として認識を試みる
    en_word_match = re.match(r"\b[a-zA-Z]+(?:'[a-zA-Z]+)?\b", text)
    if en_word_match:
        word = en_word_match.group(0)
        pos = _guess_en_pos(word)
        return Token(word, pos, Language.ENGLISH)

    # 数値として認識を試みる
    number_match = re.match(r"\b\d+(?:\.\d+)?\b", text)
    if number_match:
        return Token(number_match.group(0), "number", Language.UNKNOWN)

    # 助詞として認識を試みる
    particle_match = re.match(BASIC_PARTICLES, text)
    if particle_match:
        return Token(particle_match.group(0), "助詞", Language.JAPANESE)

    # 1文字を未知語として扱う
    lang = _detect_language(text[0])
    return Token(text[0], "unknown", lang)


def _extract_jp_features(word: str, pos: str) -> Dict[str, str]:
    """日本語トークンの追加特徴を抽出する.

    Args:
        word (str): 単語
        pos (str): 品詞

    Returns:
        Dict[str, str]: 特徴情報
    """
    features = {}

    if pos == "動詞":
        # 活用型の推定
        if word.endswith("する"):
            features["conjugation"] = "サ行変格"
        elif word.endswith(("う", "つ", "る")):
            features["conjugation"] = "五段"

    elif pos == "形容詞":
        if word.endswith("い"):
            features["type"] = "イ形容詞"
        elif word.endswith("な"):
            features["type"] = "ナ形容詞"

    return features


def _extract_en_features(word: str, pos: str) -> Dict[str, str]:
    """英語トークンの追加特徴を抽出する.

    Args:
        word (str): 単語
        pos (str): 品詞

    Returns:
        Dict[str, str]: 特徴情報
    """
    features = {}

    if pos == "verb":
        # 時制の推定
        if word.endswith("ing"):
            features["tense"] = "progressive"
        elif word.endswith("ed"):
            features["tense"] = "past"
        elif word.endswith("s"):
            features["tense"] = "present"

    elif pos == "noun":
        # 複数形の検出
        if word.endswith("s") and not word.endswith("ss"):
            features["number"] = "plural"
        else:
            features["number"] = "singular"

    return features


def _guess_en_pos(word: str) -> str:
    """英単語の品詞を推測する.

    Args:
        word (str): 単語

    Returns:
        str: 推測された品詞
    """
    if word.endswith(("tion", "sion", "ness", "ment")):
        return "noun"
    if word.endswith("ly"):
        return "adverb"
    if word.endswith(("ful", "ous", "ive", "able", "ible")):
        return "adjective"
    if word.endswith(("ize", "ise", "ate", "ify")):
        return "verb"
    return "unknown"


def _estimate_base_form(word: str, lang: Language) -> str:
    """単語の原形を推定する.

    Args:
        word (str): 単語
        lang (Language): 言語種別

    Returns:
        str: 推定された原形
    """
    if lang == Language.JAPANESE:
        # 日本語の活用語の原形推定
        for ending, base in VERB_STEM_ENDINGS:
            if word.endswith(ending):
                return word[: -len(ending)] + base
    else:
        # 英語の活用語の原形推定
        if word.endswith("ing"):
            return re.sub(r"ing$", "", word)
        if word.endswith("ed"):
            return re.sub(r"ed$", "", word)
        if word.endswith("s"):
            return re.sub(r"s$", "", word)

    return word
