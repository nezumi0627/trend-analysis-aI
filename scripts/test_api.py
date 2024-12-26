import requests


def test_analyze():
    url = "http://localhost:8000/api/analyze"
    headers = {"Content-Type": "application/json"}
    data = {
        "text": "私はPythonでAIアプリケーションを開発しています。I love programming!"
    }

    response = requests.post(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")


if __name__ == "__main__":
    test_analyze()
