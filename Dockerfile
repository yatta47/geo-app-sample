# ベースイメージとしてPython 3.12を使用
FROM python:3.12-slim

# 作業ディレクトリを作成
WORKDIR /app

# Poetryをインストール
RUN pip install poetry

# プロジェクトファイルをコンテナにコピー
COPY pyproject.toml poetry.lock /app/

# 依存関係をインストール（プロダクション環境向けの依存関係のみインストール）
RUN poetry install --no-dev --no-root

# プロジェクトのソースコードをコピー
COPY . /app

# Flaskアプリケーションを実行
CMD ["poetry", "run", "python", "app.py"]
