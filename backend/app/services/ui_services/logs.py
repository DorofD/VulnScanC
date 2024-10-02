import re


def get_logs():
    def parse_logs(log_file_path):
        """Возвращает массив словарей  [{'datetime': '2024-09-22', 'status': 'INFO', 'note': 'log_note'}]"""
        with open(log_file_path, 'r', encoding='utf-8') as file:
            logs = file.read()

        log_pattern = re.compile(
            r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (INFO|ERROR): (.+?)(?=\n\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} |\Z)', re.DOTALL)

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

        return log_list

    log_file_path = 'data/app.log'
    parsed_logs = parse_logs(log_file_path)
    return parsed_logs
