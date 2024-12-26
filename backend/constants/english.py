"""英語関連の定数定義.

英文解析に必要な様々な英語パターンを正規表現で定義したモジュール。
"""

# 基本動詞パターン
BE_VERBS = [r"\b(?:is|am|are|was|were|be|been|being)\b"]

COMMON_VERBS = (
    "\\b(?:have|has|had|do|does|did|"
    "make|made|take|took|get|got|go|went|come|came|"
    "say|said|think|thought|know|knew|see|saw|"
    "want|wanted|use|used|find|found|tell|told|"
    "ask|asked|work|worked|seem|seemed|feel|felt|"
    "try|tried|leave|left|call|called|"
    "love|loved|loves|loving)\\b"
)

# 活用語尾パターン
VERB_ENDINGS = "(?:ed|ing|s|es|en)\\b"  # 動詞活用
ADJECTIVE_ENDINGS = (
    "(?:ful|less|ous|ive|able|ible|al|ical|ic|ish|like|ly|y|ent|ant)\\b"
)
NOUN_ENDINGS = (
    "(?:tion|sion|ment|ness|ity|ance|ence|ship|hood|dom|er|or|ist|"
    "age|ure|ary|ery|ry|cy|graphy|logy|ics)\\b"
)

# 機能語パターン
PREPOSITIONS = [
    "\\b(?:"
    "in|on|at|to|for|of|with|by|"
    "from|about|into|through|after|"
    "over|between|out|against|during|"
    "without|before|under|around|among|"
    "above|across|along|behind|below|"
    "beside|beyond|down|inside|near|"
    "off|outside|past|since|toward|"
    "underneath|until|upon|within"
    ")\\b",
]

ARTICLES = [
    "\\b(?:a|an|the)\\b",
]

PRONOUNS = [
    "\\b(?:"
    "I|you|he|she|it|we|they|"
    "me|him|her|us|them|"
    "my|your|his|its|our|their|"
    "mine|yours|hers|ours|theirs|"
    "this|that|these|those|"
    "who|whom|whose|which|what|"
    "whoever|whomever|whatever|"
    "myself|yourself|himself|herself|itself|ourselves|themselves|"
    "each|other|another|some|any|many|few|all|both|"
    "none|nobody|everybody|anybody|somebody"
    ")\\b",
]

# 複合語パターン
COMPOUND_WORDS = [
    "\\b[A-Za-z]+[-][A-Za-z]+\\b",  # ハイフン付き複合語
    "\\b(?:"
    "database|software|hardware|network|"
    "website|smartphone|background|"
    "everything|something|nothing|"
    "anyone|everyone|somebody|nobody|"
    "lifestyle|workplace|hometown|"
    "worldwide|nationwide|citywide|"
    "downtown|uptown|indoor|outdoor|"
    "daytime|nighttime|lifetime|"
    "healthcare|elsewhere|nevertheless|"
    "nowadays|otherwise|meanwhile"
    ")\\b",
]

TECH_WORDS = [
    "\\b[A-Za-z]+(?:"
    "tech|net|web|app|bot|"
    "gram|book|tube|pod|cast|"
    "ware|gate|cloud|data|code|"
    "stack|base|store|space|"
    "link|chain|coin|verse|"
    "sync|flow|hub|lab|"
    "soft|cyber|crypto"
    ")\\b",
]

# 人称代名詞パターン
FIRST_PERSON_PRONOUNS = [
    "\\b(?:I|me|my|mine|we|us|our|ours|myself|ourselves)\\b"
]

SECOND_PERSON_PRONOUNS = ["\\b(?:you|your|yours|yourself|yourselves)\\b"]

THIRD_PERSON_PRONOUNS = [
    "\\b(?:he|him|his|she|her|hers|it|its|they|them|their|theirs|"
    "himself|herself|itself|themselves)\\b"
]

# 時制パターン
PRESENT_TENSE = "\\b(?:am|is|are|do|does|have|has|go|goes|make|makes)\\b"
PAST_TENSE = "\\b(?:was|were|did|had|went|made|got|took|came|gave)\\b"
FUTURE_TENSE = "\\b(?:will|shall|going to|about to|plan to|intend to)\\b"

# 法助動詞パターン
MODAL_VERBS = [
    "\\b(?:can|could|may|might|must|should|would|ought to|"
    "need to|have to|has to|supposed to)\\b"
]

# 句動詞パターン
PHRASAL_VERBS = [
    "\\b(?:look|come|go|put|take|get|make|break|give|turn|"
    "bring|call|carry|cut|fall|hold|keep|let|pick|pull|"
    "run|set|show|stand|throw|work)\\s+"
    "(?:up|down|in|out|on|off|over|away|back|through|"
    "about|across|along|around|by|for|forward|into|"
    "together|under|with)\\b"
]

# 文末表現パターン
SENTENCE_ENDINGS = [
    "\\b(?:please|right|okay|alright|indeed|exactly|absolutely|"
    "certainly|definitely|surely|actually|basically|literally)\\b",
    "\\b(?:isn't it|aren't you|don't you|won't you|"
    "couldn't you|shouldn't we|wouldn't it|"
    "am I right|you know|you see|I mean)\\b",
]

# 接続詞パターン
CONJUNCTIONS = [
    "\\b(?:and|or|but|so|for|nor|yet|"
    "because|although|though|unless|while|"
    "if|when|where|as|since|before|after|"
    "whether|whereas|however|therefore|moreover|"
    "furthermore|nevertheless|meanwhile|otherwise)\\b"
]

# 数量表現パターン
QUANTIFIERS = [
    "\\b(?:many|much|few|little|some|any|all|both|each|every|"
    "several|enough|plenty|lots|most|more|less|fewer)\\b"
]
