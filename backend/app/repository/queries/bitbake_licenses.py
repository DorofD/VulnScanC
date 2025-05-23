from app.repository.queries.base_query import execute_db_query


def add_bitbake_license(component_id, license, recipe_name):
    query = f"""
            INSERT INTO bitbake_licenses ('component_id', 'license', 'recipe_name') VALUES ('{component_id}', '{license}', '{recipe_name}');
            """
    return execute_db_query(query)


def get_bitbake_component_licenses(component_id):
    query = f"""
            SELECT * FROM bitbake_licenses
            WHERE component_id = '{component_id}'
            """
    return execute_db_query(query)


def delete_bitbake_license(id):
    query = f"""
            DELETE FROM bitbake_licenses 
            WHERE id = {id};
            """
    execute_db_query(query)
