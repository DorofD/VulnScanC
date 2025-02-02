import os
import datetime

from app.services.sec_dev_scanner.builder import build_binary


def get_binary_info():
    info_dict = {'binary_file': False,
                 'build_log_data': False, 'change_time': False}
    if os.path.exists("/binary/build.log"):
        with open("/binary/build.log", 'r') as file:
            log_data = file.read()
        info_dict['build_log_data'] = log_data

    binary_path = '/binary/executable_module'
    if os.path.exists(binary_path):
        change_time = datetime.datetime.fromtimestamp(
            os.path.getmtime(binary_path))
        info_dict['change_time'] = str(change_time)
        info_dict['binary_file'] = "/binary/executable_module"
    return info_dict


def build_executable_module():
    build_binary()
