import psycopg2.extras
import psycopg2
import os
from dotenv import load_dotenv
from pgvector.psycopg2 import register_vector


load_dotenv('.env')
DB_CONFIG = {
    'host': os.environ['POSTGRES_HOST'],
    'port': os.environ['POSTGRES_PORT'],
    'database': os.environ['POSTGRES_DB'],
    'user': os.environ['POSTGRES_USER'],
    'password': os.environ['POSTGRES_PASSWORD']
}


def execute_query(query, params=None, fetch="all"):
    """fetch: "all"|"one"|None"""
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        register_vector(conn)  # важно: до выполнения запросов с vector

        with conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params)

            if fetch == "all":
                rows = cur.fetchall()
                return [dict(r) for r in rows]

            if fetch == "one":
                row = cur.fetchone()
                return dict(row) if row is not None else None

            return None
    finally:
        conn.close()


# def execute_query(query, params=None, fetch="all"):
#     """fetch: "all"|"one"|None"""
#     conn = psycopg2.connect(**DB_CONFIG)
#     try:
#         with conn, conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
#             cur.execute(query, params)

#             if fetch == "all":
#                 rows = cur.fetchall()
#                 return [dict(r) for r in rows]

#             if fetch == "one":
#                 row = cur.fetchone()
#                 return dict(row) if row is not None else None

#             return None
#     finally:
#         conn.close()
