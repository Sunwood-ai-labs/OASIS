FROM python:3.10-slim

# 環境変数設定
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 作業ディレクトリを設定
WORKDIR /app

# 依存パッケージを先にコピーしてインストール（キャッシュ活用）
# setup.py, requirements.txt, README.md, oasisパッケージを先にコピーしてキャッシュを有効化
COPY setup.py requirements.txt README.md oasis /app/
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc firefox-esr \
    # symlink for firefox binary
    && ln -sf /usr/bin/firefox-esr /usr/bin/firefox \
    && pip install --upgrade pip \
    && pip install -e . \
    && apt-get purge -y --auto-remove gcc \
    && rm -rf /var/lib/apt/lists/*

# プロジェクトファイルをコピー
COPY . /app

# Web UI用ポート
EXPOSE 8501

# デフォルトでCLIをエントリポイントとし、Web UIモードを実行
ENTRYPOINT ["oasis"]
CMD ["--webui"]
