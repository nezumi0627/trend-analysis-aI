"""日本語の品詞パターン定義.

このモジュールは日本語の品詞パターンを正規表現で定義します。
主に形態素解析のための基本パターンを提供します。
"""

from backend.constants.common import ALPHA_NUM, SYMBOLS
from backend.constants.japanese import (
    ADJ_CONJUGATION,
    HIRAGANA,
    JAPANESE_CHARS,
    KANJI,
    KANJI_CHARS,
    KATAKANA,
    VERB_CONJUGATION,
    VERB_STEM_ENDINGS,
)

# 記号パターン
SYMBOLS = {
    "記号": [
        rf"[{SYMBOLS['括弧']}{SYMBOLS['句読点']}{SYMBOLS['感嘆符']}{SYMBOLS['その他']}]",
        rf"[{SYMBOLS.get('矢印', '')}]",  # 矢印記号
        rf"[{SYMBOLS.get('数学記号', '')}]",  # 数学記号
    ],
}

# 自立語（Independent Words）
INDEPENDENT_WORDS = {
    # 名詞（Nouns）
    "名詞": [
        # 一般名詞
        KANJI,  # 漢字
        HIRAGANA,  # ひらがな
        KATAKANA,  # カタカナ
        ALPHA_NUM,  # 英数字
        # 固有名詞
        rf"{KANJI_CHARS}{JAPANESE_CHARS}+",  # 人名・地名など
        # 数詞
        r"\d+(?:[年月日個円人回台分秒階]|[かが]?月|[かこ]?日)",
        # 複合名詞
        rf"(?:{KANJI_CHARS}|{JAPANESE_CHARS})+(?:性|化|法|式|的|論|学|者|家|場|室|所|品)",
    ],
    # 動詞（Verbs）
    "動詞": [
        # 五段活用
        rf"{JAPANESE_CHARS}+{VERB_STEM_ENDINGS}\b",
        # 活用形
        rf"{JAPANESE_CHARS}+{VERB_CONJUGATION}\b",
        # サ変動詞
        rf"(?:{JAPANESE_CHARS}+)?(?:する|される|した|された|している|されている|しよう|されよう)\b",
        # カ変動詞
        r"(?:来|き|く|こ)(?:る|れる|られる|よう|ない|させる)\b",
        # 可能動詞
        rf"{JAPANESE_CHARS}+(?:える|られる)\b",
    ],
    # 形容詞（Adjectives）
    "形容詞": [
        # イ形容詞
        rf"{JAPANESE_CHARS}+{ADJ_CONJUGATION}\b",
        # ナ形容詞（形容動詞）
        rf"{JAPANESE_CHARS}+(?:な|に|だ|で|です|でした|だった|だろう)\b",
        # タル形容詞
        rf"{JAPANESE_CHARS}+たる\b",
    ],
    # 副詞（Adverbs）
    "副詞": [
        # 一般副詞
        r"(?:"
        r"とても|非常に|かなり|少し|ちょっと|"
        r"全く|まったく|特に|既に|直ぐに|"
        r"すぐに|最も|もっと|どう|そう|"
        r"ああ|こう|やはり|確か|多分|"
        r"恐らく|きっと|必ず|絶対に|"
        r"徐々に|次第に|段々|急に|突然|"
        r"実に|本当に|正に|大変|相当"
        r")\b",
        # 形容詞派生
        rf"{JAPANESE_CHARS}+(?:く|に)\b",
        # オノマトペ
        r"(?:[あ-ん]{2})+(?:り|と)?\b",
    ],
}

# 付属語（Dependent Words）
DEPENDENT_WORDS = {
    # 助詞（Particles）
    "助詞": [
        # 格助詞
        r"(?:"
        r"が|の|を|に|へ|と|から|より|で|"
        r"による|において|について|として|"
        r"ながら|つつ|にて|をもって|において|"
        r"によって|に関して|に対して|を通じて"
        r")\b",
        # 接続助詞
        r"(?:"
        r"ば|たら|なら|ても|のに|から|"
        r"ので|けれども|けど|し|て|"
        r"ものの|ところ|ところで|とともに|"
        r"ものの|にもかかわらず|ために"
        r")\b",
        # 副助詞
        r"(?:"
        r"は|も|こそ|さえ|でも|しか|"
        r"まで|ばかり|だけ|ほど|くらい|"
        r"など|なんか|かな|よ|ね|"
        r"やら|なり|かしら|っけ|わ|ぞ|ぜ"
        r")\b",
        # 並立助詞
        r"(?:や|か|なり|だの|とか)\b",
    ],
    # 助動詞（Auxiliary Verbs）
    "助動詞": [
        # 受身・使役
        r"(?:れる|られる|せる|させる|れた|られた|せた|させた|させられる)\b",
        # 否定
        r"(?:ない|ぬ|ん|まい|なかった|ません|ませんでした)\b",
        # 丁寧
        r"(?:です|ます|でした|ました|でしょう|ましょう|ください|いただく|なさる)\b",
        # 推量・様態
        r"(?:そうだ|ようだ|らしい|かもしれない|にちがいない|はずだ|べきだ|ことができる)\b",
        # アスペクト
        r"(?:ている|てある|ておく|てしまう|ていく|てくる)\b",
    ],
}

# 特殊（Special）
SPECIAL = {
    # 接続詞（Conjunctions）
    "接続詞": [
        r"(?:"
        r"しかし|けれども|ただし|また|"
        r"および|そして|それに|それから|"
        r"したがって|それでは|すなわち|"
        r"つまり|例えば|ところで|では|"
        r"ところが|だから|そのため|"
        r"ならびに|あるいは|もしくは|"
        r"なお|ただ|但し|さらに|"
        r"というのは|なぜなら|要するに"
        r")\b",
    ],
    # 感動詞（Interjections）
    "感動詞": [
        r"(?:"
        r"あ|あっ|ああ|うん|えっ|おお|"
        r"おっ|わあ|はい|いいえ|さあ|"
        r"よし|よしよし|ええ|あら|まあ|"
        r"へえ|ふむ|なるほど|おや|"
        r"やあ|いやいや|おっと|わっ|"
        r"ありがとう|すみません|失礼|"
        r"ごめん|おめでとう|さようなら"
        r")\b",
    ],
    # 連体詞（Prenominal Adjectives）
    "連体詞": [
        r"(?:"
        r"この|その|あの|どの|"
        r"いわゆる|例の|大きな|小さな|"
        r"ある|いろんな|そんな|こんな|"
        r"あんな|どんな|たいした"
        r")\b",
    ],
}

# すべてのパターンを結合（Combine All Patterns）
JP_PATTERNS = {
    **INDEPENDENT_WORDS,
    **DEPENDENT_WORDS,
    **SPECIAL,
    **SYMBOLS,
}
