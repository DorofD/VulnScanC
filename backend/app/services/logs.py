import re
import os
log_level = os.environ['LOG_LEVEL'].lower()


def get_logs():
    def parse_logs(log_file_path):
        """Возвращает словарь  {'logs': [{'datetime': '2024-09-22', 'status': 'INFO', 'note': 'log_note'}, ...], 'log_level': str, 'count': int}"""
        with open(log_file_path, 'r', encoding='utf-8') as file:
            logs = file.read()

        if log_level == 'info':
            level_pattern = '(INFO|ERROR)'
        elif log_level == 'debug':
            level_pattern = '(INFO|ERROR|DEBUG)'
        else:
            level_pattern = '(INFO|ERROR)'

        # оригинальное выражение
        # log_pattern = re.compile(
        #     r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (INFO|ERROR|DEBUG): (.+?)(?=\n\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} |\Z)', re.DOTALL)

        expression = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) ' + level_pattern + \
            r': (.+?)(?=\n\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} |\Z)'
        log_pattern = re.compile(expression, re.DOTALL)

        matches = log_pattern.findall(logs)
        log_list = []
        for match in matches:
            log_dict = {
                'datetime': match[0],
                'status': match[1],
                'note': match[2].strip()
            }
            log_list.append(log_dict)
        log_list.reverse()
        return [log_list, level_pattern]
    log_file_path = 'data/app.log'
    parsed_logs, level_pattern = parse_logs(log_file_path)
    current_levels = level_pattern.replace('(', '').replace(')', '').split('|')

    log_file_size = os.path.getsize(log_file_path)
    log_file_size_mb = log_file_size / (1024 * 1024)
    log_file_size_str = f"{log_file_size_mb:.4f} МБ"

    result = {'logs': parsed_logs, 'level': log_level,
              'count': len(parsed_logs), 'levels': current_levels,
              'log_file_size': log_file_size_str}
    return result


def get_log_file_path():
    # hardcoded log_path is ./data/app.log
    return os.path.join(os.getcwd(), 'data', 'app.log')


def delete_logs():
    with open('data/app.log', 'r+') as f:
        f.truncate(0)
    return True
