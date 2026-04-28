from datetime import datetime

from app.pg_repository.queries.components_comments import DBComponentsComments

def add_comment_for_component(user_id, component_id, comment):
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    db_comments = DBComponentsComments()
    db_comments.add_comment(user_id, component_id, formatted_time, comment)


def get_comments_for_component(component_id):
    db_comments = DBComponentsComments()
    return db_comments.get_comments_for_component(component_id)


def delete_component_comment(id):
    db_comments = DBComponentsComments()
    db_comments.delete_comment(id)
