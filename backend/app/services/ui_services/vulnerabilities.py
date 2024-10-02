import json
import re
import ast

from app.repository.queries.vulnerabilities import get_vulnerabilities_by_component as get_vulnerabilities_by_component_db


def get_vulnerabilities_by_component(id):
    vulns = get_vulnerabilities_by_component_db(id)
    for vuln in vulns:
        vuln['full_data'] = ast.literal_eval(vuln['full_data'])

    critical_list = []
    high_list = []
    medium_list = []
    low_list = []
    not_found_list = []

    for vuln in vulns:
        if 'severity' not in vuln['full_data']:
            not_found_list.append(vuln)
            continue
        if vuln['full_data']['severity'][0]['calculated_severities']['base_severity'] == 'Critical' or vuln['full_data']['severity'][0]['calculated_severities']['environmental_severity'] == 'Critical' or vuln['full_data']['severity'][0]['calculated_severities']['temporal_severity'] == 'Critical':
            critical_list.append(vuln)
            continue
        if vuln['full_data']['severity'][0]['calculated_severities']['base_severity'] == 'High' or vuln['full_data']['severity'][0]['calculated_severities']['environmental_severity'] == 'High' or vuln['full_data']['severity'][0]['calculated_severities']['temporal_severity'] == 'High':
            high_list.append(vuln)
            continue
        if vuln['full_data']['severity'][0]['calculated_severities']['base_severity'] == 'Medium' or vuln['full_data']['severity'][0]['calculated_severities']['environmental_severity'] == 'Medium' or vuln['full_data']['severity'][0]['calculated_severities']['temporal_severity'] == 'Medium':
            medium_list.append(vuln)
            continue
        if vuln['full_data']['severity'][0]['calculated_severities']['base_severity'] == 'Low' or vuln['full_data']['severity'][0]['calculated_severities']['environmental_severity'] == 'Low' or vuln['full_data']['severity'][0]['calculated_severities']['temporal_severity'] == 'Low':
            low_list.append(vuln)
            continue
    result = [*critical_list, *high_list, *
              medium_list, *low_list, *not_found_list]
    return result
