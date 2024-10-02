import sqlite3


def execute_db_query(query, value_array=0, last_row_id=False):
    """
    по умолчанию возвращает список словарей в формате [{'field_1':'значение', 'field_2':'значение'}, ...]
    если last_row_id=True, возвращает словарь в формате {'last_row_id': id}
    если передан value_array, выполняется executemany
    """
    conn = sqlite3.connect('./data/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    if not value_array:
        cursor.execute(query)
        result = cursor.fetchall()
        if result and type(result) == list:
            result = [dict(i) for i in result]
        elif result and last_row_id:
            result = dict(result)
        elif result:
            result = dict(result)
        elif not result and last_row_id:
            result = {'last_row_id': cursor.lastrowid}
    else:
        cursor.executemany(query, value_array)
        result = True
    conn.commit()
    conn.close()
    return result
