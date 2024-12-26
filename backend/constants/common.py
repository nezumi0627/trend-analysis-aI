"""共通の定数定義.

このモジュールは、テキスト解析に必要な様々な定数を定義します。
文字パターン、区切り文字、品詞情報、解析設定など、システム全体で使用される
基本的な定数が含まれています。
"""

import re
from typing import Dict, List, Pattern

# 文字種パターン
ALPHA: Pattern = re.compile(r"[A-Za-zａ-ｚＡ-Ｚ]")  # 全角半角アルファベット
DIGIT: Pattern = re.compile(r"[0-9０-９]")  # 全角半角数字
ALPHA_NUM: Pattern = re.compile(
    rf"(?:{ALPHA.pattern}+|{DIGIT.pattern}+)"
)  # 英数字

# 区切り文字パターン
SEPARATORS: Pattern = re.compile(r"[。．.!?！？\n]+")  # 文の区切り
WHITESPACE: Pattern = re.compile(r"[\s　]+")  # 全角半角空白文字

# 記号パターン
SYMBOLS: Dict[str, Pattern] = {
    "括弧": re.compile(r"[「」『』（）\[\]｛｝\(\)\{\}〈〉《》【】]"),
    "句読点": re.compile(r"[、。，．,.]"),
    "感嘆符": re.compile(r"[！!？?‼⁉]"),
    "その他": re.compile(r"[…―:：;；・~～=＝]"),
}

# 重要度の閾値
IMPORTANCE_THRESHOLDS: Dict[str, float] = {
    "最高": 3.0,
    "高": 2.0,
    "中": 1.0,
    "低": 0.5,
    "最低": 0.1,
}

# 品詞の種類
POS_TYPES: Dict[str, List[str]] = {
    "自立語": ["名詞", "動詞", "形容詞", "形容動詞", "副詞"],
    "付属語": ["助詞", "助動詞", "接続詞", "接頭辞", "接尾辞"],
    "その他": ["記号", "感動詞", "フィラー", "未知語"],
}

# 品詞タグ
POS_TAGS: Dict[str, str] = {
    # 基本品詞
    "NOUN": "名詞",
    "VERB": "動詞",
    "ADJ": "形容詞",
    "ADV": "副詞",
    "PRON": "代名詞",
    "DET": "限定詞",
    "ADP": "前置詞/後置詞",
    "CONJ": "接続詞",
    "PART": "助詞",
    "NUM": "数詞",
    "SYM": "記号",
    # 詳細品詞
    "PROPN": "固有名詞",
    "AUX": "助動詞",
    "INTJ": "感動詞",
    "SCONJ": "従属接続詞",
    "CCONJ": "等位接続詞",
    # 人称
    "PRON_1": "一人称代名詞",
    "PRON_2": "二人称代名詞",
    "PRON_3": "三人称代名詞",
    # 時制
    "TENSE_PAST": "過去",
    "TENSE_PRESENT": "現在",
    "TENSE_FUTURE": "未来",
    # その他
    "UNKNOWN": "未知語",
}

# 解析設定
ANALYSIS_CONFIG: Dict[str, bool | int] = {
    "min_word_length": 1,  # 最小単語長
    "max_word_length": 50,  # 最大単語長
    "ignore_case": True,  # 大文字小文字を区別しない
    "normalize_text": True,  # テキストを正規化する
    "remove_stopwords": True,  # ストップワードを除去
    "lemmatize": True,  # 単語を原形に変換
    "remove_punctuation": True,  # 句読点を除去
    "remove_numbers": False,  # 数字を除去
}

# 重要度スコア
IMPORTANCE_SCORES: Dict[str, float] = {
    "NOUN": 1.0,
    "VERB": 0.8,
    "ADJ": 0.7,
    "ADV": 0.6,
    "PROPN": 1.2,
    "NUM": 0.4,
    "INTJ": 0.3,
    "UNKNOWN": 0.5,
    "SCONJ": 0.2,
    "CCONJ": 0.2,
}
