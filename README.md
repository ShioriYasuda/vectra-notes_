# **「pgvector × FastAPI のドキュメント検索API」**

PDF/テキストを登録→埋め込み生成→PostgreSQL(pgvector)に保存→クエリで意味検索、を提供する小さなAIサービス。
Python3.12 / FastAPI / SQLAlchemy / Pydantic / PostgreSQL / Docker を全部使い、Keycloak(OIDC) 認可も入れます。

## プロジェクト名案

vectra-notes（ベクタ＋ノーツ）

目的：チーム内のメモ・FAQ・要件書から「意味検索」を提供するAPI

機能（MVP → 拡張）

MVP（1〜2日）

ヘルスチェック GET /healthz

認証（Keycloakの「optional」設定で、認証ありの場合はレート緩和）

ドキュメント登録 POST /docs（テキスト/タイトル）

検索 GET /search?q=...（上位k件返す）

PostgreSQL + pgvector でベクトル格納

拡張（以降）

PDFアップロード＆テキスト抽出（pypdf）

チャンク分割（LangChain/TextSplitter相当の軽実装）

RAGっぽい回答 POST /qa（検索結果を単純要約：最初はLLMなしで抽出要約→後で好きなモデルを接続）

ユーザー/ワークスペース多 tenants

監査ログ、メトリクス(Prometheus/OpenTelemetry)

## 構成

vectra-notes/
├─ src/
│  ├─ app/
│  │  ├─ main.py               # FastAPI起動点
│  │  ├─ deps.py               # 依存注入（DB, Auth, Settings）
│  │  ├─ routers/
│  │  │  ├─ health.py
│  │  │  ├─ docs.py            # 登録・一覧
│  │  │  └─ search.py          # 検索
│  │  ├─ models/
│  │  │  ├─ base.py            # SQLAlchemy Base
│  │  │  ├─ document.py
│  │  │  └─ embedding.py
│  │  ├─ schemas/
│  │  │  ├─ document.py        # Pydantic BaseModelたち
│  │  │  └─ search.py
│  │  ├─ services/
│  │  │  ├─ embedder.py        # 埋め込み生成
│  │  │  └─ searcher.py        # pgvector検索
│  │  └─ auth/
│  │     └─ keycloak.py        # OIDC検証(JWT)
│  └─ settings.py              # pydantic-settings
├─ migrations/                 # Alembic（後で）
├─ tests/
│  ├─ test_health.py
│  ├─ test_docs.py
│  └─ test_search.py
├─ docker/
│  ├─ Dockerfile.api
│  ├─ keycloak/
│  │  ├─ Dockerfile
│  │  └─ realm-export.json     # 開発用Realm
│  └─ sql/
│     └─ 001_enable_pgvector.sql
├─ docker-compose.yml
├─ .env.example
├─ pyproject.toml
├─ README.md
└─ LICENSE


## 主要技術の選定メモ

埋め込みモデル：sentence-transformers/all-MiniLM-L6-v2（小さくてCPUで動く、pipだけでOK）

DB：PostgreSQL 16 + pgvector 拡張（cosine距離で近似検索）

Auth：Keycloak + OIDC（開発用Realmを一緒にdocker-composeで起動）

API：FastAPI + Pydantic v2 + SQLAlchemy 2.0

ツール：ruff（lint/format）、pytest、mypy（必要なら）