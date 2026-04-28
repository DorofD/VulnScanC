from app.pg_repository.queries.base_query import execute_query

class DBBitbakeLicenses():
    def __init__(self):
        pass

    def add_bitbake_license(self, component_id: int, license: str, recipe_name: str):
        query = """
            INSERT INTO bitbake_licenses (component_id, license, recipe_name)
            VALUES (%s, %s, %s)
        """
        return execute_query(query, params=(component_id, license, recipe_name))

    def get_bitbake_component_licenses(self, component_id: int):
        query = "SELECT * FROM bitbake_licenses WHERE component_id = %s"
        return execute_query(query, params=(component_id,), fetch="all")

    def delete_bitbake_license(self, license_id: int):
        query = "DELETE FROM bitbake_licenses WHERE id = %s"
        return execute_query(query, params=(license_id,))
