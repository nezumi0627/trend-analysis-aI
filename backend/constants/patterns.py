"""正規表現パターンの定数定義.

このモジュールは、テキスト処理で使用される正規表現パターンの定数を定義します。

Constants:
    SENTENCE_SEPARATORS (str): 文の区切りを検出するための正規表現パターン
    TRAILING_SYMBOLS (str): 文末の記号を検出するための正規表現パターン
    QUOTE_PAIRS (str): 引用符のペアを検出するためのパターン
    PARENTHESIS_PAIRS (str): 括弧のペアを検出するためのパターン
"""

from backend.constants.common import SYMBOLS

# 文の区切りパターン（より詳細な制御）
SENTENCE_SEPARATORS = (
    r"(?<=[。．.!?！？])\s*(?=[^」』）\]｝}、。．.!?！？]|$)|"  # 句読点後
    r"(?<=[\n])\s*(?=[^\s])|"  # 改行後
    r"(?<=」|』|）|\]|｝|})\s*(?=[^、。．.!?！？])"  # 閉じ括弧後
)

# 末尾の記号パターン
TRAILING_SYMBOLS = (
    rf"[{SYMBOLS['句読点'].pattern}"
    rf"{SYMBOLS['感嘆符'].pattern}"
    rf"{SYMBOLS['括弧'].pattern}]$"
)

# 引用符のペアパターン
QUOTE_PAIRS = r"「.*?」|『.*?』"

# 括弧のペアパターン
PARENTHESIS_PAIRS = r"（.*?）|\(.*?\)|\[.*?\]|｛.*?｝|\{.*?\}"
