import json
import os
from ldap3 import Connection
from dotenv import load_dotenv
from app.repository.queries.users import get_user_db, get_users_db, add_user_db, delete_user_db, change_user_db


def ldap_auth(login: str, password: str):
    load_dotenv('.env')
    LDAP_SERVER = os.environ['LDAP_SERVER']
    LDAP_USER = os.environ['LDAP_USER']
    LDAP_PASSWORD = os.environ['LDAP_PASSWORD']
    LDAP_USER_CN = os.environ['LDAP_USER_CN']
    SEARCH_USER_CATALOG = os.environ['SEARCH_USER_CATALOG']
    SEARCH_BASE = os.environ['SEARCH_BASE']
    try:
        conn = Connection(server=LDAP_SERVER, user=LDAP_USER_CN,
                          auto_bind=True, password=LDAP_PASSWORD)

        conn.search(search_filter=f'(sAMAccountName={login})',
                    search_base=SEARCH_BASE, )
        entry = json.loads(conn.entries[0].entry_to_json())
        user_dn = entry['dn']
        conn = Connection(server=LDAP_SERVER, user=user_dn,
                          password=password, raise_exceptions=True)
        if conn.bind():
            return True
        return False
    except:
        return False


def local_auth(login: str, password: str):
    pass


def signin(login: str, password: str):
    user = get_user_db(login)
    if not user:
        return False
    user = user[0]
    if user['auth_type'] == 'ldap':
        if ldap_auth(login, password):
            return {'id': user['id'], 'login': login, 'role': user['role']}
        return False
    elif user['auth_type'] == 'local':
        if password == user['password']:
            return {'id': user['id'], 'login': login, 'role': user['role']}
        return False
    else:
        raise Exception(
            f"Unknown user auth_type in function signin: {user['auth_type']}")


def get_users():
    return get_users_db()


def add_user(login: str, auth_type: str, role: str, password: str):
    if auth_type == 'ldap':
        add_user_db(login, auth_type, role)
    elif auth_type == 'local':
        add_user_db(login, auth_type, role, password)
    else:
        raise Exception(
            f'Received unknown auth type when adding a user: {auth_type}')


def change_user(id: int, login: str, role: str, auth_type: str, password: str):
    if auth_type == 'local':
        if password:
            changes = {'login': login, 'role': role, 'password': password}
        else:
            changes = {'login': login, 'role': role}
    else:
        changes = {'login': login, 'role': role}
    change_user_db(id, changes)


def delete_user(id: int):
    delete_user_db(id=id)
