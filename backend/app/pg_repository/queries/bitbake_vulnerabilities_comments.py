from app.pg_repository.queries.base_query import execute_query

class DBBitbakeVulnerabilitiesComments():
    def __init__(self):
        pass

    def add_bitbake_vulnerability_comment(self, user_id: int, vuln_id: int, datetime_str: str, comment: str):
        query = """
            INSERT INTO bitbake_vulnerabilities_comments (user_id, vuln_id, datetime, comment)
            VALUES (%s, %s, %s, %s)
        """
        return execute_query(query, params=(user_id, vuln_id, datetime_str, comment))

    def get_bitbake_comments_for_vulnerability(self, vuln_id: int):
        query = """
            SELECT cc.*, u.login AS user_name
            FROM bitbake_vulnerabilities_comments cc
            JOIN users u ON cc.user_id = u.id
            WHERE cc.vuln_id = %s
        """
        return execute_query(query, params=(vuln_id,), fetch="all")

    def delete_bitbake_vulnerability_comment(self, comment_id: int):
        query = "DELETE FROM bitbake_vulnerabilities_comments WHERE id = %s"
        return execute_query(query, params=(comment_id,))
