"""助詞の定数定義.

日本語の助詞を分類ごとに定義したモジュール。
文の解析や自然言語処理に使用される基本的な助詞を含む。
"""

# 主要な助詞
CASE_PARTICLES = ["は", "が", "を", "に", "へ", "で"]  # 格助詞
BINDING_PARTICLES = ["も", "と", "や", "か", "など", "やら"]  # 並立助詞
ENDING_PARTICLES = ["ね", "よ", "な", "わ", "ぞ", "ぜ", "さ"]  # 終助詞
ADVERBIAL_PARTICLES = ["から", "まで", "ばかり", "だけ", "ほど"]  # 副助詞
CONJUNCTIVE_PARTICLES = ["が", "けれども", "のに", "ので"]  # 接続助詞

# 重要度が高い助詞（文の主要な要素を示す助詞）
IMPORTANT_PARTICLES = CASE_PARTICLES + [
    "から",
    "まで",
]  # 文の骨格を形成する助詞

# 複合助詞（二つ以上の助詞が組み合わさったもの）
COMPOUND_PARTICLES = ["について", "によって", "として", "にとって"]

# 助詞の全セット（重複を除去）
ALL_PARTICLES = list(
    set(
        CASE_PARTICLES
        + BINDING_PARTICLES
        + ENDING_PARTICLES
        + ADVERBIAL_PARTICLES
        + CONJUNCTIVE_PARTICLES
        + COMPOUND_PARTICLES
    )
)
