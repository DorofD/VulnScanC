from app.repository.queries.base_query import execute_db_query


def add_bitbake_vulnerability_comment(user_id, vuln_id, datetime, comment):
    query = f"""
            INSERT INTO bitbake_vulnerabilities_comments ('user_id', 'vuln_id', 'datetime', 'comment') VALUES  ('{user_id}', '{vuln_id}', '{datetime}', '{comment}');
            """
    return execute_db_query(query)


def get_bitbake_comments_for_vulnerability(vuln_id):
    query = f"""
            SELECT cc.*, u.login AS user_name
            FROM bitbake_vulnerabilities_comments cc
            JOIN users u ON cc.user_id = u.id
            WHERE cc.vuln_id = '{vuln_id}'
            """
    return execute_db_query(query)


def delete_bitbake_vulnerability_comment(id):
    query = f"""
            DELETE FROM bitbake_vulnerabilities_comments
            WHERE id = {id}; 
            """
    return execute_db_query(query)
