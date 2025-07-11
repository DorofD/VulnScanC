import sqlite3


def create_db():
    conn = sqlite3.connect('./data/database.db')
    query = """
            CREATE TABLE IF NOT EXISTS "users" (
                "id"	INTEGER NOT NULL UNIQUE,
                "login"	TEXT NOT NULL UNIQUE,
                "auth_type"	TEXT NOT NULL,
                "role"	TEXT NOT NULL,
                "password"	TEXT,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
            """
    cursor = conn.cursor()
    cursor.execute(query)

    query = """
            CREATE TABLE IF NOT EXISTS "projects" (
                "id"	INTEGER NOT NULL UNIQUE,
                "name"	TEXT NOT NULL UNIQUE,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
            """
    cursor = conn.cursor()
    cursor.execute(query)

    query = """
            CREATE TABLE IF NOT EXISTS "components" (
                "id"	INTEGER NOT NULL UNIQUE,
                "project_id"	INTEGER NOT NULL,
                "path"	TEXT NOT NULL,
                "type"	TEXT,
                "address"	TEXT,
                "tag"	TEXT,
                "version"	TEXT,
                "score"	REAL,
                "status"	INTEGER NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT),
                FOREIGN KEY("project_id") REFERENCES "projects"("id")
            );
            """
    cursor = conn.cursor()
    cursor.execute(query)

    query = """
            CREATE TABLE IF NOT EXISTS "vulnerabilities" (
                "id"	INTEGER NOT NULL UNIQUE,
                "component_id"	INTEGER NOT NULL,
                "osv_id"	TEXT,
                "full_data"	TEXT,
                PRIMARY KEY("id" AUTOINCREMENT),
                FOREIGN KEY("component_id") REFERENCES "components"("id")
            );
            """
    cursor = conn.cursor()
    cursor.execute(query)

    query = """
            CREATE TABLE IF NOT EXISTS "snapshots" (
                "id"	INTEGER NOT NULL UNIQUE,
                "project_id"	INTEGER NOT NULL,
                "datetime"	TEXT NOT NULL,
                "components"	TEXT,
                PRIMARY KEY("id" AUTOINCREMENT),
                FOREIGN KEY("project_id") REFERENCES "projects"("id")
            );
            """
    cursor = conn.cursor()
    cursor.execute(query)

    query = """
            CREATE TABLE IF NOT EXISTS "licenses" (
                "id"	INTEGER NOT NULL UNIQUE,
                "component_id"	INTEGER,
                "key"	TEXT,
                "name"	TEXT,
                "spdx_id"	TEXT,
                "url"	TEXT,
                FOREIGN KEY("component_id") REFERENCES "components"("id"),
                PRIMARY KEY("id" AUTOINCREMENT)
            );
            """
    cursor = conn.cursor()
    cursor.execute(query)

    query = """
            CREATE TABLE IF NOT EXISTS "bdu_vulnerabilities" (
                "id"	INTEGER NOT NULL UNIQUE,
                "component_id"	INTEGER NOT NULL,
                "component_type"	TEXT NOT NULL,
                "bdu_id"	TEXT NOT NULL,
                "cve_id"	TEXT NOT NULL,
                "name"	TEXT,
                "description"	TEXT,
                "status"	TEXT,
                "bdu_severity"	TEXT,
                "severity"	TEXT,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
            """
    cursor = conn.cursor()
    cursor.execute(query)

    query = """
                CREATE TABLE IF NOT EXISTS "components_comments" (
                    "id"	INTEGER NOT NULL UNIQUE,
                    "user_id"	INTEGER NOT NULL,
                    "component_id"	INTEGER NOT NULL,
                    "datetime"	TEXT NOT NULL,
                    "comment"	TEXT,
                    FOREIGN KEY("user_id") REFERENCES "users"("id"),
                    FOREIGN KEY("component_id") REFERENCES "components"("id"),
                    PRIMARY KEY("id" AUTOINCREMENT)
                );
            """
    cursor = conn.cursor()
    cursor.execute(query)

    query = """
                CREATE TABLE IF NOT EXISTS "bitbake_components_comments" (
                    "id"	INTEGER NOT NULL UNIQUE,
                    "user_id"	INTEGER NOT NULL,
                    "component_id"	INTEGER NOT NULL,
                    "datetime"	TEXT NOT NULL,
                    "comment"	TEXT,
                    FOREIGN KEY("user_id") REFERENCES "users"("id"),
                    FOREIGN KEY("component_id") REFERENCES "bitbake_components"("id"),
                    PRIMARY KEY("id" AUTOINCREMENT)
                );
            """
    cursor = conn.cursor()
    cursor.execute(query)

    query = """
                CREATE TABLE IF NOT EXISTS "bitbake_vulnerabilities_comments" (
                    "id"	INTEGER NOT NULL UNIQUE,
                    "user_id"	INTEGER NOT NULL,
                    "vuln_id"	INTEGER NOT NULL,
                    "datetime"	TEXT NOT NULL,
                    "comment"	TEXT,
                    FOREIGN KEY("user_id") REFERENCES "users"("id"),
                    FOREIGN KEY("vuln_id") REFERENCES "bitbake_vulnerabilities"("id"),
                    PRIMARY KEY("id" AUTOINCREMENT)
                );
            """
    cursor = conn.cursor()
    cursor.execute(query)

    query = """
                CREATE TABLE IF NOT EXISTS "bitbake_projects" (
                    "id"	INTEGER NOT NULL UNIQUE,
                    "name"	TEXT NOT NULL,
                    PRIMARY KEY("id" AUTOINCREMENT)
                );
            """
    cursor = conn.cursor()
    cursor.execute(query)

    query = """
                CREATE TABLE IF NOT EXISTS "bitbake_snapshots" (
                    "id"	INTEGER NOT NULL UNIQUE,
                    "project_id"	INTEGER NOT NULL,
                    "datetime"	TEXT NOT NULL,
                    "components"	TEXT,
                    PRIMARY KEY("id" AUTOINCREMENT),
                    FOREIGN KEY("project_id") REFERENCES "bitbake_projects"("id")
                );
            """
    cursor = conn.cursor()
    cursor.execute(query)

    query = """
                CREATE TABLE IF NOT EXISTS "bitbake_components" (
                    "id"	INTEGER NOT NULL UNIQUE,
                    "project_id"	INTEGER NOT NULL,
                    "name"	TEXT,
                    "version"	TEXT,
                    "layer"	TEXT,
                    PRIMARY KEY("id" AUTOINCREMENT),
                    FOREIGN KEY("project_id") REFERENCES "bitbake_projects"("id")
                );
            """
    cursor = conn.cursor()
    cursor.execute(query)

    query = """
                CREATE TABLE IF NOT EXISTS "bitbake_vulnerabilities" (
                    "id"	INTEGER NOT NULL UNIQUE,
                    "component_id"	INTEGER NOT NULL,
                    "cve"	TEXT NOT NULL,
                    "status"	TEXT,
                    "summary"	TEXT,
                    "cvss_v2"	TEXT,
                    "cvss_v3"	TEXT,
                    "severity"  TEXT,
                    "vector"	TEXT,
                    "more_information"	TEXT,
                    PRIMARY KEY("id" AUTOINCREMENT),
                    FOREIGN KEY("component_id") REFERENCES ""
                );
            """
    cursor = conn.cursor()
    cursor.execute(query)

    query = """
                CREATE TABLE IF NOT EXISTS "bitbake_licenses" (
                    "id"	INTEGER NOT NULL UNIQUE,
                    "component_id"	INTEGER NOT NULL,
                    "license"	TEXT,
                    "recipe_name"	TEXT,
                    PRIMARY KEY("id" AUTOINCREMENT),
                    FOREIGN KEY("component_id") REFERENCES "bitbake_components"("id")
                );
            """
    cursor = conn.cursor()
    cursor.execute(query)
