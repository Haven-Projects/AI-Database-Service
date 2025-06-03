import os
from sqlalchemy import create_engine


db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASS")
db_host = os.environ.get("DB_HOST")
db_name = os.environ.get("DB_NAME")

print("Trying to connect with:", db_user, "@", db_host, "/", db_name)

# Include port explicitly if needed:
connection_string = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:3306/{db_name}"
engine = create_engine(connection_string)

try:
    with engine.connect() as conn:
        result = conn.execute("SELECT 1;")
        print("Connection OK, result:", result.fetchall())
except Exception as e:
    print("Error connecting:", e)
