import psycopg2
import os
from dotenv import load_dotenv


load_dotenv('.env')
DB_CONFIG = {
    'host': os.environ['POSTGRES_HOST'],
    'port': os.environ['POSTGRES_PORT'],
    'database': os.environ['POSTGRES_DB'],
    'user': os.environ['POSTGRES_USER'],
    'password': os.environ['POSTGRES_PASSWORD']
}


def create_db():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            login TEXT NOT NULL UNIQUE,
            auth_type TEXT NOT NULL,
            role TEXT NOT NULL,
            password TEXT);
        """)

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS rag_chunks (
          id bigserial PRIMARY KEY,
          chunk_number int NOT NULL,
          source_document_name text NOT NULL,
          raw_text text NOT NULL,
          meta jsonb DEFAULT '{{}}'::jsonb,
          embedding vector(1024) NOT NULL
        );
        """)

    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS rag_chunks_uniq
        ON rag_chunks (source_document_name, chunk_number);
        """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS rag_chunks_embedding_hnsw
        ON rag_chunks
        USING hnsw (embedding vector_cosine_ops);
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS llama_chat_nodes (
        id bigserial PRIMARY KEY,
        uuid uuid NOT NULL DEFAULT gen_random_uuid(),
        name text,
        base_api_url text NOT NULL,
        description text,
        created_at timestamptz NOT NULL DEFAULT now()
        );
                   """)

    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS llama_chat_nodes_uuid_uniq
        ON llama_chat_nodes (uuid);
                   """)

    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS llama_chat_nodes_base_api_url_uniq
        ON llama_chat_nodes (base_api_url);
                   """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS llama_embedding_nodes (
        id bigserial PRIMARY KEY,
        uuid uuid NOT NULL DEFAULT gen_random_uuid(),
        name text,
        base_api_url text NOT NULL,
        description text,
        created_at timestamptz NOT NULL DEFAULT now()
        );
                   """)

    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS llama_embedding_nodes_uuid_uniq
        ON llama_embedding_nodes (uuid);
                   """)

    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS llama_embedding_nodes_base_api_url_uniq
        ON llama_embedding_nodes (base_api_url);
                   """)

    cursor.close()
    conn.close()
