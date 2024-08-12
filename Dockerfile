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

# ポート番号の情報提供用にEXPOSEを追加
EXPOSE 5000

# Flaskアプリケーションを起動するコマンド
# `PORT` 環境変数を使って起動するポートを指定
CMD ["sh", "-c", "poetry run flask run --host=0.0.0.0 --port=${PORT}"]