"""トレンド分析アプリケーション.

テキストの分析とトレンド抽出を行うFlaskアプリケーション。
"""

from typing import Dict, List, Union

from flask import Flask, Response, jsonify, render_template, request
from flask_cors import CORS

from backend.config.settings import STATIC_DIR, TEMPLATE_DIR
from backend.constants.colors import GRAY, POS_COLORS
from backend.core.database import get_db
from backend.patterns import (
    preprocess_text,
    split_sentences,
    tokenize_sentence,
)
from backend.services.trend.analyzer import TrendAnalyzer
from backend.services.trend.scoring.trend_scoring import TrendScoring
from backend.utils.logger import setup_logger

# アプリケーション初期化
app = Flask(
    __name__, template_folder=str(TEMPLATE_DIR), static_folder=str(STATIC_DIR)
)
CORS(app)

# ロガー設定
logger = setup_logger()

# サービス初期化
analyzer = TrendAnalyzer()
scoring = TrendScoring()


@app.route("/")
def index() -> str:
    """メインページを表示する.

    Returns:
        str: レンダリングされたHTMLテンプレート
    """
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze() -> tuple[Response, int]:
    """テキストを分析する.

    Returns:
        tuple[Response, int]: JSON形式の分析結果とステータスコード
    """
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify({"error": "不正なリクエスト形式です"}), 400

        text = data.get("text", "").strip()
        if not text:
            return jsonify({"error": "テキストが空です"}), 400

        # テキストの前処理と分析
        text = preprocess_text(text)
        sentences = split_sentences(text)

        # 分析結果
        analysis_result: List[List[Dict[str, Union[str, float]]]] = []

        for sentence in sentences:
            words = tokenize_sentence(sentence)
            sentence_analysis = []

            for word in words:
                # Tokenオブジェクトから必要な情報を抽出
                word_info = {
                    "word": word.text,
                    "pos": word.pos,
                    "importance": analyzer._identify_part_of_speech(str(word))[
                        1
                    ],
                    "color": get_pos_color(word.pos),
                    "language": str(word.language).split(".")[1]
                    if word.language
                    else "UNKNOWN",
                    "is_compound": word.is_compound,
                    "original_form": word.original_form,
                }
                sentence_analysis.append(word_info)

            analysis_result.append(sentence_analysis)

        # トレンドの更新
        with get_db() as db:
            trends = analyzer.update_trends(db, text)

        return jsonify(
            {
                "result": analysis_result,
                "patterns": analyzer.get_patterns(),
                "trends": trends,
            }
        )

    except Exception as e:
        logger.error(f"分析中にエラーが発生: {e}", exc_info=True)
        return jsonify({"error": "内部サーバーエラーが発生しました"}), 500


@app.route("/api/trends/popular")
def get_popular_trends() -> tuple[Response, int]:
    """人気のトレンドを取得する.

    Returns:
        tuple[Response, int]: JSON形式のトレンドデータとステータスコード
    """
    try:
        with get_db() as db:
            trends = scoring.get_top_trends(db)
            return jsonify({"trends": trends})
    except Exception as e:
        logger.error(f"人気トレンド取得中にエラーが発生: {e}", exc_info=True)
        return jsonify({"error": "内部サーバーエラーが発生しました"}), 500


@app.route("/api/trends/latest")
def get_latest_trends() -> tuple[Response, int]:
    """最新のトレンドを取得する.

    Returns:
        tuple[Response, int]: JSON形式のトレンドデータとステータスコード
    """
    try:
        with get_db() as db:
            trends = scoring.get_latest_trends(db)
            return jsonify({"trends": trends})
    except Exception as e:
        logger.error(f"最新トレンド取得中にエラーが発生: {e}", exc_info=True)
        return jsonify({"error": "内部サーバーエラーが発生しました"}), 500


def get_pos_color(pos: str) -> str:
    """品詞に応じた色を返す.

    Args:
        pos (str): 品詞

    Returns:
        str: 対応する色のコード
    """
    return POS_COLORS.get(pos, GRAY)  # デフォルトはグレー


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
