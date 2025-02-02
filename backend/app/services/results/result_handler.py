"""
vulns_search_result schema:
    directory
    match
        score
        repo_info
            type
            address
            tag
            version
            commit

    vulns
        [0]
            id
            details
            modified
            published
            references
                [0]
                    type
                    url
            ?severity
                [0]
                    type
                    score
                    ?calculated_severities
"""


def handle_vulns(vulns_search_result: list, output_mode: str, output_file: str = None):
    """output_mode ожидает строку 'file' или 'console', в зависимости от режима результат будет записан в файл или выведен в консоль"""
    def format_note(note):
        formatted_note = (
            f"PATH IN PROJECT: {note['directory']}\n"
            '\n'
            f"MATCH LIBRARY:\n"
            f"Score: {note['match']['score']}\n"
            f"Type: {note['match']['repo_info']['type']}\n"
            f"Address: {note['match']['repo_info']['address']}\n"
            f"Tag: {note['match']['repo_info']['tag']}\n"
            f"Version: {note['match']['repo_info']['version']}\n"
            '\n'
            "VULNERABILITIES: \n"
        )

        for vuln in note['vulns']:
            formatted_note += f"ID: {vuln['id']} \n"

            formatted_note += "Details: \n"
            formatted_note += f"{vuln['details']} \n"
            formatted_note += '\n'

            if 'references' in vuln:
                formatted_note += "References: \n"
                for reference in vuln['references']:
                    formatted_note += f"{reference['url']} \n"
                formatted_note += '\n'
            if 'severity' in vuln:
                formatted_note += "Severity: \n"
                formatted_note += f"Score: {vuln['severity'][0]['score']} \n"

                if 'calculated_severities' in vuln['severity'][0]:
                    formatted_note += f"Base severity: {vuln['severity'][0]['calculated_severities']['base_severity']} \n"
                    formatted_note += f"Temporal severity: {vuln['severity'][0]['calculated_severities']['temporal_severity']} \n"
                    formatted_note += f"Environmental severity: {vuln['severity'][0]['calculated_severities']['environmental_severity']} \n"
                else:
                    formatted_note += f"Severities can't be calculate \n"
                formatted_note += '\n'
            else:
                formatted_note += "Severity: no one was found\n"

        formatted_note += '\n'
        formatted_note += '\n'
        formatted_note += '\n'

        return formatted_note

    if output_mode == 'console':
        print('\n')
        print("Vulerabilities search result:")
        print('\n')
        for note in vulns_search_result:
            print(format_note(note))
    elif output_mode == 'file' and output_file:
        with open(output_file, 'w') as file:
            for note in vulns_search_result:
                file.write(format_note(note))
    else:
        print('The mode is specified incorrectly or the output file is not specified')


def handle_matches(matches_search_result: list, output_mode: str, output_file: str = None):
    """output_mode ожидает строку 'file' или 'console', в зависимости от режима результат будет записан в файл или выведен в консоль"""

    def format_note(note):
        formatted_note = (
            f"PATH IN PROJECT: {note['directory']}\n"
            f"MATCH: {note['match']['repo_info']['address']}\n"
            f"TAG: {note['match']['repo_info']['tag']}\n"
            f"VERSION: {note['match']['repo_info']['version']}\n"
            f"SCORE: {note['match']['score']}\n"
            '\n'
            '\n'
        )
        return formatted_note

    if output_mode == 'console':
        print('\n')
        print("Matches search result:")
        print('\n')
        for note in matches_search_result:
            print(format_note(note))
    elif output_mode == 'file' and output_file:
        with open(output_file, 'w') as file:
            for note in matches_search_result:
                file.write(format_note(note))
    else:
        print('The mode is specified incorrectly or the output file is not specified')
