import psycopg

conn = psycopg.connect(
    host="localhost",
    port=5433,
    dbname="clinical_ops_db",
    user="clinical_ops_user",
    password="ClinicalUser123"
)

with conn.cursor() as cur:
    cur.execute("SELECT current_database(), current_user, 1;")
    print(cur.fetchone())

conn.close()