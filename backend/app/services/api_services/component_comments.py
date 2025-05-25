from datetime import datetime

from app.repository.queries.components_comments import add_comment as add_comment_db
from app.repository.queries.components_comments import get_comments_for_component as get_comments_for_component_db
from app.repository.queries.components_comments import delete_comment as delete_comment_db


def add_comment_for_component(user_id, component_id, comment):
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    add_comment_db(user_id, component_id, formatted_time, comment)


def get_comments_for_component(component_id):
    return (get_comments_for_component_db(component_id))


def delete_component_comment(id):
    delete_comment_db(id)
