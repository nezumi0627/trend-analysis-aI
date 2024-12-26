"""色の定数定義.

このモジュールは、アプリケーション全体で使用される色の定数を定義します。
色はHEX形式で指定され、品詞タグ付けの視覚化に使用されます。
"""

from typing import Dict, Final

# 基本色
GRAY: Final[str] = "#999999"
BLACK: Final[str] = "#000000"
WHITE: Final[str] = "#FFFFFF"
RED: Final[str] = "#F44336"

# アクセント色
PRIMARY: Final[str] = "#2196F3"
SECONDARY: Final[str] = "#FF9800"
SUCCESS: Final[str] = "#4CAF50"
WARNING: Final[str] = "#FFC107"
ERROR: Final[str] = RED

# 品詞別の色
POS_COLORS: Dict[str, str] = {
    # 日本語
    "名詞": SUCCESS,  # 緑 - 実体を表す重要な品詞
    "代名詞": "#8BC34A",  # 薄緑 - 名詞の代用
    "動詞": PRIMARY,  # 青 - 動作・状態を表す重要な品詞
    "形容詞": SECONDARY,  # オレンジ - 性質・状態を表す修飾語
    "形容動詞": "#FF5722",  # ディープオレンジ - 形容詞に準ずる
    "副詞": "#9C27B0",  # 紫 - 様態・程度などの修飾語
    "連体詞": "#795548",  # 茶色 - 名詞を修飾
    "助詞": "#757575",  # グレー - 文法的な機能語
    "助動詞": "#607D8B",  # ブルーグレー - 文末表現など
    "接続詞": "#795548",  # 茶色 - 文をつなぐ
    "感動詞": "#E91E63",  # ピンク - 感情表現
    "記号": GRAY,  # グレー - 句読点など
    # 英語
    "noun": SUCCESS,  # 緑
    "pronoun": "#8BC34A",  # 薄緑
    "verb": PRIMARY,  # 青
    "adjective": SECONDARY,  # オレンジ
    "adverb": "#9C27B0",  # 紫
    "preposition": "#757575",  # グレー
    "conjunction": "#795548",  # 茶色
    "article": "#757575",  # グレー
    "determiner": "#795548",  # 茶色
    "interjection": "#E91E63",  # ピンク
    "symbol": GRAY,  # グレー
}
