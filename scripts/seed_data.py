"""テストデータ生成スクリプト.

より現実的なトレンドデータを生成するためのスクリプト。
時間による重み付けやカテゴリ分類を考慮し、自然なトレンドの分布を実現する。
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
import secrets
from datetime import UTC, datetime, timedelta
from enum import Enum, auto
from typing import Dict, List, NamedTuple, Tuple

from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.models import Base, Trend

# デバッグ設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# データベース設定
SQLALCHEMY_DATABASE_URL = "sqlite:///./trends.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
Base.metadata.create_all(bind=engine)

# Faker設定
fake = Faker(["ja_JP", "en_US"])


class KeywordCategory(Enum):
    """キーワードのカテゴリを定義."""

    TECH = auto()
    BUSINESS = auto()
    SOCIAL = auto()
    RANDOM = auto()


class KeywordData(NamedTuple):
    """キーワードに関連するデータを格納する構造体."""

    count: int
    created_at: datetime
    category: KeywordCategory


# 基本キーワードリスト（カテゴリごとの重要度を追加）
TECH_KEYWORDS: List[Tuple[str, float]] = [
    ("AI", 1.5),
    ("機械学習", 1.3),
    ("ブロックチェーン", 1.2),
    ("クラウド", 1.2),
    ("Python", 1.4),
    ("データ分析", 1.3),
    ("セキュリティ", 1.2),
    ("IoT", 1.1),
    ("5G", 1.2),
    ("量子コンピュータ", 1.3),
]

BUSINESS_KEYWORDS: List[Tuple[str, float]] = [
    ("スタートアップ", 1.4),
    ("投資", 1.3),
    ("マーケティング", 1.2),
    ("DX", 1.5),
    ("SDGs", 1.3),
    ("サブスクリプション", 1.2),
    ("フィンテック", 1.3),
    ("働き方改革", 1.2),
    ("リモートワーク", 1.4),
]

SOCIAL_KEYWORDS: List[Tuple[str, float]] = [
    ("サステナビリティ", 1.4),
    ("再生可能エネルギー", 1.3),
    ("教育", 1.2),
    ("医療", 1.3),
    ("地方創生", 1.2),
    ("多様性", 1.3),
    ("ウェルネス", 1.2),
    ("メタバース", 1.3),
    ("NFT", 1.2),
]


def weighted_choice(choices: List[str], weights: List[float]) -> str:
    """重み付きの選択を行う.

    Args:
        choices (List[str]): 選択肢のリスト
        weights (List[float]): 各選択肢に対応する重みのリスト

    Returns:
        str: 選択された要素
    """
    total = int(sum(weights))
    cumulative_weights = [sum(weights[: i + 1]) for i in range(len(weights))]
    rand_val = secrets.randbelow(total)
    for choice, cumulative_weight in zip(choices, cumulative_weights):
        if rand_val < cumulative_weight:
            return choice
    return choices[-1]  # デフォルトで最後の選択肢を返す


def generate_keyword() -> Tuple[str, KeywordCategory, float]:
    """キーワードを生成する.

    Returns:
        Tuple[str, KeywordCategory, float]:
        キーワード、カテゴリ、重要度係数のタプル
    """
    category_weights = {
        KeywordCategory.TECH: 0.35,
        KeywordCategory.BUSINESS: 0.30,
        KeywordCategory.SOCIAL: 0.25,
        KeywordCategory.RANDOM: 0.10,
    }

    # secretsを使用してカテゴリを選択
    total = int(sum(category_weights.values()))
    choice = secrets.randbelow(total)
    cumulative = 0

    for _, weight in category_weights.items():
        cumulative += weight * 100
        if choice < cumulative:
            break

    category = weighted_choice(
        [category.name for category in category_weights],
        list(category_weights.values()),
    )
    category = KeywordCategory[category]  # 文字列からKeywordCategoryに変換

    if category == KeywordCategory.TECH:
        keyword, importance = fake.random_element(elements=TECH_KEYWORDS)
        return keyword, category, importance
    if category == KeywordCategory.BUSINESS:
        keyword, importance = fake.random_element(elements=BUSINESS_KEYWORDS)
        return keyword, category, importance
    if category == KeywordCategory.SOCIAL:
        keyword, importance = fake.random_element(elements=SOCIAL_KEYWORDS)
        return keyword, category, importance

    # ランダムなキーワード生成（より多様な生成方法）
    keyword_style = fake.random_element(
        elements=[
            ("company", 0.3),
            ("catch_phrase", 0.3),
            ("hashtag", 0.2),
            ("buzzword", 0.2),
        ]
    )

    if keyword_style == "company":
        return fake.company(), category, 1.0
    if keyword_style == "catch_phrase":
        return fake.catch_phrase(), category, 1.0
    if keyword_style == "buzzword":
        return fake.bs(), category, 1.0
    return f"#{fake.word()}", category, 0.8


def calculate_trend_score(
    count: int, created_at: datetime, now: datetime, importance: float
) -> float:
    """レンドスコアを計算する.

    Args:
        count (int): 投稿数
        created_at (datetime): 作成日時
        now (datetime): 現在時刻
        importance (float): 重要度係数

    Returns:
        float: 計算されたトレンドスコア
    """
    hours_old = (now - created_at).total_seconds() / 3600

    # 時間による重み付け（より洗練された減衰関数）
    time_weight = 1.0 / (1.0 + (hours_old / 12) ** 1.5)

    # 投稿数による対数スケーリング
    count_weight = (1 + count) ** 0.7

    # 最終スコアの計算
    return round(count_weight * time_weight * importance * 10, 2)


def generate_test_data(session: Session, num_posts: int = 1000) -> None:
    """テストデータを生成する.

    Args:
        session (Session): データベースセッション
        num_posts (int): 生成する投稿数
    """
    now = datetime.now(UTC)

    # より細かい投稿の分布を設定
    count_ranges = [
        (1, 30),  # 40%: 一般的な投稿
        (31, 100),  # 30%: やや話題の投稿
        (101, 300),  # 20%: 話題の投稿
        (301, 700),  # 8%: 人気の投稿
        (701, 1500),  # 2%: バイラルの投稿
    ]

    # キーワードとの投稿数を追跡
    keyword_data: Dict[str, KeywordData] = {}

    for _ in range(num_posts):
        # より自然な時間分布を生成
        hours_ago = abs(fake.normal(loc=12, scale=4))
        hours_ago = min(max(0.1, hours_ago), 24)  # 0.1-24時間の範囲に制限
        created_at = now - timedelta(hours=hours_ago)

        # キーワードを生成
        keyword, category, importance = generate_keyword()

        # 投稿数の範囲を決定（より現実的な分布）
        probability = secrets.randbelow(100)
        range_index = (
            0
            if probability < 40
            else 1
            if probability < 70
            else 2
            if probability < 90
            else 3
            if probability < 98
            else 4
        )
        count_range = count_ranges[range_index]

        # 投稿数を生成（より自然な分布）
        base_count = (
            secrets.randbelow(count_range[1] - count_range[0] + 1)
            + count_range[0]
        )
        post_count = int(base_count * importance)

        # キーワードの出現回数を更新
        if keyword in keyword_data:
            current_data = keyword_data[keyword]
            keyword_data[keyword] = KeywordData(
                count=current_data.count + post_count,
                created_at=max(created_at, current_data.created_at),
                category=current_data.category,
            )
        else:
            keyword_data[keyword] = KeywordData(
                count=post_count, created_at=created_at, category=category
            )

    # トレンドを生成
    for keyword, data in keyword_data.items():
        score = calculate_trend_score(
            data.count,
            data.created_at,
            now,
            importance=1.2 if data.category != KeywordCategory.RANDOM else 1.0,
        )

        trend = Trend(
            keyword=keyword,
            count=data.count,
            score=score,
            created_at=data.created_at,
        )
        session.add(trend)

    session.commit()
    logger.info(
        f"{num_posts}件の投稿から{len(keyword_data)}件のトレンドを生成しました"
    )

    # カテゴリごとの統計を出力
    category_stats = {category: 0 for category in KeywordCategory}
    for data in keyword_data.values():
        category_stats[data.category] += 1

    for category, count in category_stats.items():
        logger.info(f"{category.name}: {count}件")


if __name__ == "__main__":
    with Session(engine) as session:
        # 既存のデータをクリア
        session.query(Trend).delete()
        session.commit()

        # 1000投稿分のデータを生成
        generate_test_data(session, num_posts=1000)
