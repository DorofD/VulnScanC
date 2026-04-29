import requests
from cvss import CVSS3, CVSS4
from cvss import exceptions as cvss_exceptions


def calculate_severities(vector):
    try:
        c = CVSS3(vector)
        return {'base_severity': c.severities()[0], 'temporal_severity': c.severities()[1], 'environmental_severity': c.severities()[2]}
    except cvss_exceptions.CVSS3MalformedError:
        c = CVSS4(vector)
        return {'base_severity': c.severity, 'temporal_severity': c.severity, 'environmental_severity': c.severity}


class OsvClient:
    def search_by_commit(self, commit: str) -> dict:
        response = requests.post('https://api.osv.dev/v1/query',
                                 json={"commit": commit})
        return response.json()

    def determine_version(self, data: dict) -> dict:
        response = requests.post(
            'https://api.osv.dev/v1experimental/determineversion', json=data)
        return response.json()
