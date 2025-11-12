
import requests
from cvss import CVSS3, CVSS4
from cvss import exceptions as cvss_exceptions
import copy
print('sas')


def calculate_severities(vector):

    try:
        c = CVSS3(vector)
        return {'base_severity': c.severities()[0], 'temporal_severity': c.severities()[1], 'environmental_severity': c.severities()[2]}
    except cvss_exceptions.CVSS3MalformedError:
        c = CVSS4(vector)
        return {'base_severity': c.severity, 'temporal_severity': c.severity, 'environmental_severity': c.severity}
    # print(c.severities())


def search_vulnerabilities(dirs_matches: list):
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
            response = requests.post('https://api.osv.dev/v1/query',
                                     json={"commit": matches[i]['match']['repo_info']['commit']})
            if not 'vulns' in response.json():
                continue
            matches[i]['vulns'] = response.json()['vulns']
            for vuln in matches[i]['vulns']:
                if 'severity' in vuln and 'score' in vuln['severity'][0]:
                    calculated_severities = calculate_severities(
                        vuln['severity'][0]['score'])

                    vuln['severity'][0]['calculated_severities'] = calculated_severities
            result.append(matches[i])
    return result
