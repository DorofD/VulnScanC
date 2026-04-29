import copy
from app.adapters.osv_client import OsvClient, calculate_severities


class VulnFinder:
    def __init__(self):
        self.osv_client = OsvClient()

    def search_vulnerabilities(self, dirs_matches: list) -> list:
        """
        возвращает список словарей в формате [{'directory':'директория библиотеки в проекте',
                                        'match':'наиболее точное совпадение',
                                        'vulns': 'список уязвимостей'}]
        если в библиотеке уязвимости не обнаружены - запись не будет включена в возвращаемый список
        """
        matches = copy.deepcopy(dirs_matches)
        result = []
        if matches:
            for i in range(len(matches)):
                response = self.osv_client.search_by_commit(
                    matches[i]['match']['repo_info']['commit'])
                if not 'vulns' in response:
                    continue
                matches[i]['vulns'] = response['vulns']
                for vuln in matches[i]['vulns']:
                    if 'severity' in vuln and 'score' in vuln['severity'][0]:
                        calculated_severities = calculate_severities(
                            vuln['severity'][0]['score'])

                        vuln['severity'][0]['calculated_severities'] = calculated_severities
                result.append(matches[i])
        return result
