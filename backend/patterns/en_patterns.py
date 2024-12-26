"""英語の品詞パターン定義.

英文の形態素解析のための正規表現パターン集。
独立語(Content Words)と機能語(Function Words)に大別し、
各品詞ごとにパターンを定義している。
"""

from backend.constants.common import ALPHA, SYMBOLS
from backend.constants.english import (
    ADJECTIVE_ENDINGS,
    BE_VERBS,
    COMMON_VERBS,
    NOUN_ENDINGS,
    VERB_ENDINGS,
)

# 記号（Punctuation）
SYMBOLS = {
    "punctuation": [
        rf"[{SYMBOLS['句読点']}{SYMBOLS['感嘆符']}{SYMBOLS['その他']}]",
        r"[" "''" "'']+",  # 引用符
        r"[-–—]+",  # ハイフン・ダッシュ
    ],
}

# 自立語（Content Words）
INDEPENDENT_WORDS = {
    # 名詞（Nouns）
    "noun": [
        # 固有名詞（大文字で始まる）
        rf"\b[A-Z]{ALPHA}[a-z]+\b",
        # 複合名詞
        rf"\b{ALPHA}[a-z]+[-\s]{ALPHA}[a-z]+\b",
        # 派生名詞
        rf"\b[a-z]+{NOUN_ENDINGS}",
        # 一般的な名詞
        r"\b(?:"
        r"data|system|user|time|way|day|year|"
        r"people|man|woman|child|world|life|work|"
        r"part|place|case|group|company|number|"
        r"problem|fact|thing|name|area|family|"
        r"question|study|business|issue|point|"
        r"government|money|service|information"
        r")\b",
    ],
    # 動詞（Verbs）
    "verb": [
        BE_VERBS,
        COMMON_VERBS,
        # 活用形
        rf"\b[a-z]+{VERB_ENDINGS}",
        # 句動詞
        r"\b(?:look|come|go|put|take|get|make|set)\s+(?:up|down|in|out|off|on|away|back)\b",
    ],
    # 形容詞（Adjectives）
    "adjective": [
        # 派生形容詞
        rf"\b[a-z]+{ADJECTIVE_ENDINGS}",
        # 複合形容詞
        r"\b[a-z]+[-][a-z]+(?:ed|ing)\b",
        # 基本形容詞
        r"\b(?:"
        r"good|bad|big|small|high|low|"
        r"new|old|great|important|different|"
        r"same|right|wrong|true|false|"
        r"happy|sad|beautiful|difficult|"
        r"easy|hard|possible|impossible|"
        r"long|short|young|strong|weak|"
        r"early|late|full|empty|rich|poor|"
        r"hot|cold|warm|cool|clean|dirty"
        r")\b",
    ],
    # 副詞（Adverbs）
    "adverb": [
        # -ly副詞
        r"\b[a-z]+ly\b",
        # 程度副詞
        r"\b(?:extremely|incredibly|absolutely|completely|totally)\b",
        # 一般的な副詞
        r"\b(?:"
        r"very|really|quite|rather|too|"
        r"also|just|only|even|still|"
        r"again|already|often|always|"
        r"never|ever|sometimes|usually|"
        r"perhaps|maybe|now|then|here|"
        r"there|today|tomorrow|yesterday|"
        r"well|quickly|slowly|carefully|"
        r"together|apart|anyway|somehow"
        r")\b",
    ],
}

# 機能語（Function Words）
FUNCTION_WORDS = {
    # 前置詞（Prepositions）
    "preposition": [
        r"\b(?:"
        r"in|on|at|to|for|of|with|by|"
        r"from|about|into|through|after|"
        r"over|between|out|against|during|"
        r"without|before|under|around|among|"
        r"across|behind|beyond|within|throughout|"
        r"despite|except|like|near|opposite"
        r")\b",
    ],
    # 冠詞（Articles）
    "article": [
        r"\b(?:a|an|the)\b",
    ],
    # 代名詞（Pronouns）
    "pronoun": [
        # 人称代名詞
        r"\b(?:"
        r"I|you|he|she|it|we|they|"
        r"me|him|her|us|them|"
        r"my|your|his|its|our|their|"
        r"mine|yours|hers|ours|theirs"
        r")\b",
        # 指示代名詞
        r"\b(?:this|that|these|those)\b",
        # 疑問代名詞・関係代名詞
        r"\b(?:who|whom|whose|which|what)\b",
        # 不定代名詞
        r"\b(?:all|any|both|each|every|few|many|none|some|several)\b",
    ],
    # 接続詞（Conjunctions）
    "conjunction": [
        r"\b(?:"
        r"and|or|but|so|because|if|when|while|"
        r"although|unless|since|as|than|whether"
        r")\b",
    ],
}

# すべてのパターンを結合（Combine All Patterns）
EN_PATTERNS = {
    **INDEPENDENT_WORDS,
    **FUNCTION_WORDS,
    **SYMBOLS,
}
