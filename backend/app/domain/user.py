import json
import os
from ldap3 import Connection, ALL_ATTRIBUTES
from dotenv import load_dotenv
import traceback


class User():
    def __init__(self):
        load_dotenv('.env')
        self.server = os.environ['LDAP_SERVER']
        self.user = os.environ['LDAP_USER']
        self.password = os.environ['LDAP_PASSWORD']
        self.user_cn = os.environ['LDAP_USER_CN']
        self.search_user_catalog = os.environ['SEARCH_USER_CATALOG']
        self.search_base = os.environ['SEARCH_BASE']

    def ldap_auth(self, login: str, password: str):
        load_dotenv('.env')
        try:
            conn = Connection(server=self.server, user=self.user_cn,
                              auto_bind=True, password=self.password)

            search_filter = f'(sAMAccountName={login})'
            attributes_to_search = [
                # "sAMAccountName",
                # "userPrincipalName",
                "displayName",
                "givenName",
                "sn",
                "mail",
                # "telephoneNumber",
                # "department",
                # "title",
                # "memberOf",
            ]

            # отсеивание атрибутов, отсутствующих в схеме LDAP сервера
            schema = conn.server.schema
            available_attrs = list(schema.attribute_types.keys())
            filtered_attrs = [
                attr for attr in attributes_to_search if attr in available_attrs]

            conn.search(search_base=self.search_base,
                        search_filter=search_filter,
                        attributes=filtered_attrs)
            if not conn.entries:
                return {'success': False, 'error':  f"User '{login}' not found in LDAP"}

            entry = json.loads(conn.entries[0].entry_to_json())
            user_dn = entry['dn']

            conn = Connection(server=self.server,
                              user=user_dn, password=password)
            if conn.bind():
                for atr in entry['attributes']:
                    # аттрибуты из ldap приходят в виде списков
                    if entry['attributes'][atr] and type(entry['attributes'][atr]) == list:
                        entry['attributes'][atr] = entry['attributes'][atr][0]
                return {'success': True, 'user_data': entry['attributes']}
            return {'success': False, 'error': f"Bind failed for user {login}"}
        except Exception as exc:
            print(exc, '--', traceback.format_exc())
            return {'success': False, 'error': f"Exception in ldap_auth: {exc} -- {traceback.format_exc()}"}

    def get_password_hash(self, password):
        pass

    def local_auth(self, login: str, password: str):
        pass

    def signin(self, login, password, user_note):
        if user_note['auth_type'] == 'ldap':
            auth_result = self.ldap_auth(login, password)
            if auth_result['success']:
                auth_result['user_data']['id'] = user_note['id']
                auth_result['user_data']['login'] = login
                auth_result['user_data']['role'] = user_note['role']
                auth_result['user_data']['auth_type'] = user_note['auth_type']
            return auth_result
        if user_note['auth_type'] == 'local':
            if password == user_note['password']:
                user_data = {'id': user_note['id'],
                             'login': login,
                             'role': user_note['role'],
                             'auth_type': user_note['auth_type']}
                return {'success': True, 'user_data': user_data}
            return {'success': False, 'error': "Wrong password"}
        return {'success': False, 'error': f"User {login} has unknown auth_type - {user_note['auth_type']}"}
