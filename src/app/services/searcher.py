from sqlalchemy import text
from sqlalchemy.orm import Session

def cosine_similarity_sql() -> str:
    # ARRAYベースの簡易cos類似（学習用）。pgvectorなら <-> でOK。
    return """
      1 - (
        (SELECT SUM(a*b) FROM UNNEST(e.vector) WITH ORDINALITY AS v1(a, i)
         JOIN UNNEST(:query) WITH ORDINALITY AS v2(b, j) ON i=j)
        /
        (sqrt((SELECT SUM(a*a) FROM UNNEST(e.vector) AS a))
         * sqrt((SELECT SUM(b*b) FROM UNNEST(:query) AS b)))
      )
    """

def top_k(session: Session, qvec: list[float], k: int = 5):
    sql = text(f"""
      SELECT d.id, d.title, {cosine_similarity_sql()} AS dist
      FROM embeddings e
      JOIN documents d ON d.id = e.doc_id
      ORDER BY dist ASC
      LIMIT :k
    """)
    return session.execute(sql, {"query": qvec, "k": k}).mappings().all()
