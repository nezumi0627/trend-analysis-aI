"""日本語関連の定数定義.

日本語の文字種、助詞、活用などの正規表現パターンを定義するモジュール。
"""

# 文字種の基本パターン
HIRAGANA_CHARS = "[ぁ-ん]"  # ひらがな
KATAKANA_CHARS = "[ァ-ン]"  # カタカナ
KANJI_CHARS = "[一-龯]"  # 漢字
JAPANESE_CHARS = "[ぁ-んァ-ン一-龯]"  # 日本語文字全般

# 文字種の拡張パターン
HIRAGANA = "[ぁ-んー・゛゜]+"  # ひらがな（長音、中黒、濁点、半濁点含む）
KATAKANA = "[ァ-ンー・゛゜]+"  # カタカナ（長音、中黒、濁点、半濁点含む）
KANJI = "[一-龯々〆ヶ]+"  # 漢字（踊り字、特殊記号含む）

# 助動詞パターン
AUXILIARY_VERBS = [
    # 完了・進行
    "(?:していました|していません|されていました|されていません|しておきました|しておりました)\\b",
    "(?:しています|していた|されています|されていた|しておく|しておる)\\b",
    # 受身・使役・可能
    "(?:れる|られる|せる|させる|れた|られた|せた|させた|できる|できた)\\b",
    # 否定
    "(?:ない|ぬ|ん|まい|なかった|ありません|ございません)\\b",
    # 丁寧・謙譲・尊敬
    "(?:です|ます|でした|ました|でしょう|ましょう|ください|いただく|なさる)\\b",
    # 推量・様態・伝聞
    "(?:そうだ|ようだ|らしい|かもしれない|にちがいない|とのことだ|とされる)\\b",
]

# 複合助詞パターン
COMPOUND_PARTICLES = [
    "(?:については|によって|として|ながら|までに|までの|への|からの|"
    "によると|に関して|において|に対して|をもって|にとって)\\b",
]

# 活用パターン
VERB_STEM_ENDINGS = [
    ("う", "う"),
    ("く", "く"),
    ("ぐ", "ぐ"),
    ("す", "す"),
    ("つ", "つ"),
    ("ぬ", "ぬ"),
    ("ぶ", "ぶ"),
    ("む", "む"),
    ("る", "る"),
]

VERB_CONJUGATION = (
    "(?:ない|ます|ました|まして|ません|ませんでした|"
    "たい|たく|たかった|られる|られた|させる|させた|"
    "そうだ|そうです|たがる|てある|ている|ておく|てしまう)"
)  # 動詞活用

ADJ_CONJUGATION = (
    "(?:い|く|かった|くて|くない|かったです|"
    "くありません|くありませんでした|"
    "そうだ|そうです|がる|めだ|すぎる)"
)  # 形容詞活用

# 基本助詞パターン
BASIC_PARTICLES = "[はがをのにへとでもや]"  # 基本的な助詞

# 人称代名詞パターン
FIRST_PERSON_PRONOUNS = [
    "私|わたし|わたくし|僕|ぼく|俺|おれ|あたし|"
    "自分|じぶん|我々|われわれ|私達|わたしたち|"
    "僕達|ぼくたち|俺達|おれたち|あたしたち|"
    "小生|拙者|手前|わし|あたくし"
]

SECOND_PERSON_PRONOUNS = [
    "あなた|君|きみ|お前|おまえ|貴方|"
    "あんた|あなた方|君達|きみたち|お前達|"
    "おまえたち|あなたがた|きみがた|"
    "貴殿|貴女|そちら|お宅|皆様|みなさま"
]

THIRD_PERSON_PRONOUNS = [
    "彼|かれ|彼女|かのじょ|あの人|あのかた|"
    "彼ら|かれら|彼女達|かのじょたち|"
    "あの人達|あのかたがた|この方|その方|"
    "あの方|どなた|だれ|誰|どちら"
]

# 敬語パターン
HONORIFIC_PREFIXES = "(?:お|ご|御)"
HONORIFIC_SUFFIXES = (
    "(?:さん|様|君|さま|殿|どの|氏|先生|" "方|かた|たち|ども|各位|諸氏)"
)

# 文末表現パターン
SENTENCE_ENDINGS = [
    # 丁寧体
    "(?:です|ます|でした|ました|でしょう|ましょう)(?:ね|よ|な|かな|わ|ぞ|ぜ)?\\b",
    # 普通体
    "(?:だ|である|だった|であった|のだ|のです|なのだ|なのです)(?:ね|よ|な|かな|わ|ぞ|ぜ)?\\b",
    # その他
    "(?:とのこと|とされる|とみられる|らしい|みたいだ|ようだ)(?:ね|よ|な|かな|わ)?\\b",
]
