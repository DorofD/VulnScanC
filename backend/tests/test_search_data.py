import json
import unittest
from unittest.mock import patch, MagicMock
import requests
from app.services.search_data.search_data import SearchDataService


class TestSearchDataService(unittest.TestCase):
    def setUp(self):
        with open('tests/test_data/test_deps.json', 'r') as f:
            deps_data = json.load(f)
        with open('tests/test_data/test_vulns.json', 'r') as f:
            vulns_data = json.load(f)

        self.test_data = {
            'status': 'ok',
            'pipeline_id': 1234,
            'project_name': 'bibos',
            'datetime': '13_08_2024_17_00',
            'dependencies': deps_data,
            'vulnerabilities': vulns_data
        }

    def test_send_data_to_server(self):
        server_address = '192.168.1.134:5001'
        url = f'http://{server_address}/search_data'
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers, json=self.test_data)

        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['message'], 'Data processed successfully')

    @patch('app.services.search_data.search_data.DBSnapshots')
    @patch('app.services.search_data.search_data.DBVulnerabilities')
    @patch('app.services.search_data.search_data.DBComponents')
    @patch('app.services.search_data.search_data.DBProjects')
    def test_save_search_data_happy_path(
        self, mock_db_projects, mock_db_components,
        mock_db_vulnerabilities, mock_db_snapshots
    ):
        # --- mock project ---
        mock_db_projects_instance = MagicMock()
        mock_db_projects_instance.get_projects.return_value = [
            {'id': 1, 'name': 'bibos'}
        ]
        mock_db_projects.return_value = mock_db_projects_instance

        # --- mock components (existing) ---
        mock_db_components_instance = MagicMock()
        mock_db_components_instance.get_project_components.return_value = [
            {'id': 10, 'path': '/app/libA'},
            {'id': 11, 'path': '/app/libB'},
        ]
        mock_db_components.return_value = mock_db_components_instance

        # --- mock vulnerabilities ---
        mock_db_vulnerabilities_instance = MagicMock()
        mock_db_vulnerabilities_instance.get_vulnerabilities_by_components.return_value = []
        mock_db_vulnerabilities.return_value = mock_db_vulnerabilities_instance

        # --- mock snapshots ---
        mock_db_snapshots_instance = MagicMock()
        mock_db_snapshots.return_value = mock_db_snapshots_instance

        service = SearchDataService()
        result = service.save_search_data(self.test_data)

        self.assertTrue(result)

        # project was looked up
        mock_db_projects_instance.get_projects.assert_called_once()

        # existing components were fetched
        mock_db_components_instance.get_project_components.assert_called_once_with(
            1)

        # new components were added (those not in existing paths)
        add_component_calls = mock_db_components_instance.add_component.call_args_list
        self.assertGreater(len(add_component_calls), 0)

        # vulnerabilities were checked
        mock_db_vulnerabilities_instance.get_vulnerabilities_by_components.assert_called_once()

        # snapshot was created
        mock_db_snapshots_instance.add_snapshot.assert_called_once()

    @patch('app.services.search_data.search_data.DBSnapshots')
    @patch('app.services.search_data.search_data.DBVulnerabilities')
    @patch('app.services.search_data.search_data.DBComponents')
    @patch('app.services.search_data.search_data.DBProjects')
    def test_save_search_data_project_not_found(
        self, mock_db_projects, mock_db_components,
        mock_db_vulnerabilities, mock_db_snapshots
    ):
        mock_db_projects.return_value.get_projects.return_value = [
            {'id': 1, 'name': 'other_project'}
        ]

        service = SearchDataService()
        with self.assertRaises(Exception) as ctx:
            service.save_search_data(self.test_data)
        self.assertIn('Project not found', str(ctx.exception))

    @patch('app.services.search_data.search_data.DBSnapshots')
    @patch('app.services.search_data.search_data.DBVulnerabilities')
    @patch('app.services.search_data.search_data.DBComponents')
    @patch('app.services.search_data.search_data.DBProjects')
    def test_save_search_data_no_new_components(
        self, mock_db_projects, mock_db_components,
        mock_db_vulnerabilities, mock_db_snapshots
    ):
        mock_db_projects.return_value.get_projects.return_value = [
            {'id': 1, 'name': 'bibos'}
        ]

        # All dependency directories already exist as components
        mock_db_components.return_value.get_project_components.return_value = [
            {'id': 10, 'path': d['directory']}
            for d in self.test_data['dependencies']
        ]
        mock_db_vulnerabilities.return_value.get_vulnerabilities_by_components.return_value = []

        service = SearchDataService()
        result = service.save_search_data(self.test_data)

        self.assertTrue(result)
        # No new components should be added
        mock_db_components.return_value.add_component.assert_not_called()

    @patch('app.services.search_data.search_data.DBSnapshots')
    @patch('app.services.search_data.search_data.DBVulnerabilities')
    @patch('app.services.search_data.search_data.DBComponents')
    @patch('app.services.search_data.search_data.DBProjects')
    def test_save_search_data_adds_new_vulnerabilities(
        self, mock_db_projects, mock_db_components,
        mock_db_vulnerabilities, mock_db_snapshots
    ):
        mock_db_projects.return_value.get_projects.return_value = [
            {'id': 1, 'name': 'bibos'}
        ]
        mock_db_components.return_value.get_project_components.return_value = [
            {'id': 10, 'path': '/app/libA'}
        ]
        # No existing OSV vulns
        mock_db_vulnerabilities.return_value.get_vulnerabilities_by_components.return_value = []

        service = SearchDataService()
        service.save_search_data(self.test_data)

        # add_vulnerabilities should be called with new vulns
        mock_db_vulnerabilities.return_value.add_vulnerabilities.assert_called_once()


if __name__ == '__main__':
    unittest.main()
