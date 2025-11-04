from sqlalchemy import create_engine, text
from settings import settings

u = str(settings.DATABASE_URL)
print("URL =", u)
e = create_engine(u, future=True, pool_pre_ping=True)

try:
    with e.connect() as c:
        print("? SUCCESS: Connected to DB")
        print("DB VERSION =", c.execute(text("select version()")).scalar())
except Exception as ex:
    print("? ERROR:", ex)
