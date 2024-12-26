// トレンド関連の機能を実装
document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('trend-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const legendToggle = document.getElementById('legend-toggle');
    const legendContainer = document.getElementById('legend-container');

    // Ctrl + Enter でも分析を実行
    input.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            analyzeText();
        }
    });

    // 分析ボタンのクリックイベント
    analyzeBtn.addEventListener('click', analyzeText);

    // 凡例のトグル機能
    if (legendToggle && legendContainer) {
        legendToggle.addEventListener('click', () => {
            legendContainer.classList.toggle('active');
        });

        // 凡例の外側をクリックしたら閉じる
        document.addEventListener('click', (e) => {
            if (!legendContainer.contains(e.target) && !legendToggle.contains(e.target)) {
                legendContainer.classList.remove('active');
            }
        });
    }
});

// テキスト分析を実行する関数
async function analyzeText() {
    const input = document.getElementById('trend-input');
    const text = input.value.trim();

    if (!text) {
        alert('テキストを入力してください。');
        return;
    }

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text }),
        });

        if (!response.ok) {
            throw new Error('API request failed');
        }

        const data = await response.json();
        console.log('Received data:', data); // デバッグ用

        // 形態素解析結果の表示
        if (data.result) {
            displayAnalyzedText(data.result);
        } else {
            console.error('No result data received');
        }

        // トレンドの更新
        if (data.trends) {
            updateTrends(data.trends);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('分析中にエラーが発生しました。');
    }
}

// トレンドを更新する関数
function updateTrends(trends) {
    updateTrendSection('popular-trends', trends.popular || []);
    updateTrendSection('latest-trends', trends.latest || []);
}

// トレンドセクションを更新する関数
function updateTrendSection(sectionId, trends) {
    const container = document.getElementById(sectionId);
    const template = document.getElementById('trend-template');

    container.innerHTML = '';

    trends.forEach(trend => {
        const card = template.content.cloneNode(true);

        card.querySelector('h3').textContent = trend.keyword;
        card.querySelector('.count').textContent = `${trend.count}回`;
        card.querySelector('.score').textContent = trend.score ? `${trend.score}点` : '-';
        if (trend.created_at) {
            card.querySelector('.created-at').textContent = new Date(trend.created_at).toLocaleString();
        }

        container.appendChild(card);
    });
}

// 分析結果を表示する関数
function displayAnalyzedText(results) {
    const container = document.getElementById('analyzed-text');
    const resultContainer = document.getElementById('analysis-result');

    if (!container || !resultContainer) {
        console.error('Required elements not found');
        return;
    }

    // コンテナをクリア
    container.innerHTML = '';

    // 文ごとに処理
    results.forEach((sentence, sentenceIndex) => {
        const sentenceDiv = document.createElement('div');
        sentenceDiv.className = 'mb-4 leading-loose';

        // 文内の各単語を処理
        sentence.forEach((token, tokenIndex) => {
            const span = document.createElement('span');
            span.className = `analyzed-word pos-${token.pos.toLowerCase()}`;
            span.textContent = token.word;

            // ツールチップ情報の設定
            const info = [
                `品詞: ${token.pos}`,
                `重要度: ${token.importance.toFixed(1)}`
            ].join(' | ');
            span.setAttribute('data-info', info);

            // 単語間のスペース調整
            if (tokenIndex < sentence.length - 1) {
                const nextToken = sentence[tokenIndex + 1];
                if (shouldAddSpace(token, nextToken)) {
                    const space = document.createElement('span');
                    space.textContent = ' ';
                    sentenceDiv.appendChild(space);
                }
            }

            sentenceDiv.appendChild(span);
        });

        container.appendChild(sentenceDiv);
    });

    // 結果表示領域を表示
    resultContainer.classList.remove('hidden');
    resultContainer.classList.add('visible');

    // デバッグ情報
    console.log('Analysis results displayed:', {
        sentences: results.length,
        containerContent: container.innerHTML
    });
}

// 単語間にスペースを入れるべきかを判定
function shouldAddSpace(currentToken, nextToken) {
    if (!currentToken || !nextToken) return false;

    // 英語の単語間にはスペースを入れる
    const currentIsEnglish = /^[a-zA-Z]+$/.test(currentToken.word);
    const nextIsEnglish = /^[a-zA-Z]+$/.test(nextToken.word);

    if (currentIsEnglish && nextIsEnglish) {
        return true;
    }

    // 英語と日本語の境界にもスペースを入れる
    const currentIsJapanese = /[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]/.test(currentToken.word);
    const nextIsJapanese = /[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]/.test(nextToken.word);

    if ((currentIsEnglish && nextIsJapanese) || (currentIsJapanese && nextIsEnglish)) {
        return true;
    }

    // 記号の後にはスペースを入れない
    if (currentToken.pos === '記号' || currentToken.pos === 'symbol' ||
        currentToken.pos === 'punctuation') {
        return false;
    }

    return false;
}
