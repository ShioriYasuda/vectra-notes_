# 開発用に公式Keycloakをベースにする
FROM quay.io/keycloak/keycloak:25.0.6

# (任意) 文字化け回避のためのロケール
ENV LANG=C.UTF-8

# 開発用Realmを同梱（ファイルは後述の realm-export.json）
# Keycloakは start-dev --import-realm で /opt/keycloak/data/import 配下を自動インポートする
COPY realm-export.json /opt/keycloak/data/import/realm-export.json

# コンテナ起動時のデフォルトコマンド
# - start-dev: 開発モード
# - --import-realm: 初回起動時に上記のRealmをインポート
# - --http-enabled=true: 8080でHTTP待受（dev用途）
ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]
CMD ["start-dev", "--import-realm", "--http-enabled=true"]
