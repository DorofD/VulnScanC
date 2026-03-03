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
    cursor.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")

    cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            login TEXT NOT NULL UNIQUE,
            auth_type TEXT NOT NULL,
            role TEXT NOT NULL,
            password TEXT);
        """)

    cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS rag_documents (
                    id bigserial PRIMARY KEY,
                    uuid uuid NOT NULL DEFAULT gen_random_uuid(),
                    name text NOT NULL,
                    file_path text NULL,
                    description text NULL
                );
                """)

    cursor.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS rag_documents_uuid_uniq
                ON rag_documents (uuid);
                """)

    cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS rag_chunks (
                    id bigserial PRIMARY KEY,
                    uuid uuid NOT NULL DEFAULT gen_random_uuid(),
                    document_id bigserial NOT NULL REFERENCES rag_documents(id) ON DELETE CASCADE,
                    raw_text text NOT NULL,
                    meta jsonb DEFAULT '{{}}'::jsonb,
                    embedding vector(1024) NOT NULL
                );
                """)

    cursor.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS rag_chunks_uuid_uniq
                ON rag_chunks (uuid);
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
        created_at timestamptz NOT NULL DEFAULT now(),
        is_active boolean NOT NULL DEFAULT false
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
        CREATE UNIQUE INDEX IF NOT EXISTS llama_chat_nodes_active_uniq
        ON llama_chat_nodes (is_active)
        WHERE is_active = true;
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

    cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS projects (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE
                );
                """)

    cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS components (
                    id SERIAL PRIMARY KEY,
                    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
                    path TEXT NOT NULL,
                    type TEXT,
                    address TEXT,
                    tag TEXT,
                    version TEXT,
                    score DOUBLE PRECISION,
                    status INTEGER NOT NULL
                );
                """)

    cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS vulnerabilities (
                    id SERIAL PRIMARY KEY,
                    component_id INTEGER NOT NULL REFERENCES components(id) ON DELETE CASCADE,
                    osv_id TEXT,
                    full_data TEXT
                );
                """)

    cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS snapshots (
                    id SERIAL PRIMARY KEY,
                    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
                    datetime timestamptz NOT NULL,
                    components jsonb
                );
                """)

    cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS licenses (
                    id SERIAL PRIMARY KEY,
                    component_id INTEGER REFERENCES components(id) ON DELETE CASCADE,
                    key TEXT,
                    name TEXT,
                    spdx_id TEXT,
                    url TEXT
                );
                """)

    cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS bdu_vulnerabilities (
                    id SERIAL PRIMARY KEY,
                    component_id INTEGER NOT NULL REFERENCES components(id) ON DELETE CASCADE,
                    component_type TEXT NOT NULL,
                    bdu_id TEXT NOT NULL,
                    cve_id TEXT NOT NULL,
                    name TEXT,
                    description TEXT,
                    status TEXT,
                    bdu_severity TEXT,
                    severity TEXT
                );
                """)

    cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS components_comments (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    component_id INTEGER NOT NULL REFERENCES components(id) ON DELETE CASCADE,
                    datetime timestamptz NOT NULL,
                    comment TEXT
                );
                """)

    cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS bitbake_projects (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL
                );
                """)

    cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS bitbake_snapshots (
                    id SERIAL PRIMARY KEY,
                    project_id INTEGER NOT NULL REFERENCES bitbake_projects(id) ON DELETE CASCADE,
                    datetime timestamptz NOT NULL,
                    components jsonb
                );
                """)
    cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS bitbake_components (
                    id SERIAL PRIMARY KEY,
                    project_id INTEGER NOT NULL REFERENCES bitbake_projects(id) ON DELETE CASCADE,
                    name TEXT,
                    version TEXT,
                    layer TEXT
                );
                """)

    cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS bitbake_vulnerabilities (
                    id SERIAL PRIMARY KEY,
                    component_id INTEGER NOT NULL REFERENCES bitbake_components(id) ON DELETE CASCADE,
                    cve TEXT NOT NULL,
                    status TEXT,
                    summary TEXT,
                    cvss_v2 TEXT,
                    cvss_v3 TEXT,
                    severity TEXT,
                    vector TEXT,
                    more_information TEXT
                );
                """)

    cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS bitbake_components_comments (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    component_id INTEGER NOT NULL REFERENCES bitbake_components(id) ON DELETE CASCADE,
                    datetime timestamptz NOT NULL,
                    comment TEXT
                );
                """)

    cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS bitbake_vulnerabilities_comments (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    vuln_id INTEGER NOT NULL REFERENCES bitbake_vulnerabilities(id) ON DELETE CASCADE,
                    datetime timestamptz NOT NULL,
                    comment TEXT
                );
                """)

    cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS bitbake_licenses (
                    id SERIAL PRIMARY KEY,
                    component_id INTEGER NOT NULL REFERENCES bitbake_components(id) ON DELETE CASCADE,
                    license TEXT,
                    recipe_name TEXT
                );
                """)

    cursor.close()
    conn.close()
