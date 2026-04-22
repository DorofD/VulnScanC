import unittest
from unittest.mock import patch, MagicMock, mock_open
import xml.etree.ElementTree as ET
from app.services.fstec.bdu_fstec import FSTEC

class TestFSTEC(unittest.TestCase):
    def setUp(self):
        self.fstec = FSTEC()
        self.fstec.bdu_file = "/tmp/test_bdu.xml"

    @patch('requests.get')
    @patch('os.path.exists')
    @patch('os.remove')
    @patch('builtins.open', new_callable=mock_open)
    @patch('zipfile.ZipFile')
    def test_update_bdu_success(self, mock_zipfile, mock_file, mock_remove, mock_exists, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.iter_content.return_value = [b"chunk1", b"chunk2"]
        mock_get.return_value = mock_response
        mock_exists.return_value = True
        mock_zip_instance = mock_zipfile.return_value.__enter__.return_value
        mock_zip_instance.namelist.return_value = ["export/vulxml.xml"]
        mock_xml_content = b"<xml>content</xml>"
        mock_zip_instance.open.return_value.__enter__.return_value.read.return_value = mock_xml_content
        self.fstec.update_bdu()
        mock_get.assert_called_once()
        mock_remove.assert_called()
        mock_file.assert_any_call(self.fstec.bdu_file, "wb")

    @patch('requests.get')
    @patch('os.path.exists')
    @patch('os.remove')
    def test_update_bdu_download_fail(self, mock_remove, mock_exists, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        mock_exists.return_value = False
        with self.assertRaisesRegex(Exception, "Couldn't download FSTEC BDU"):
            self.fstec.update_bdu()

    @patch('requests.get')
    @patch('os.path.exists')
    @patch('os.remove')
    @patch('builtins.open', new_callable=mock_open)
    @patch('zipfile.ZipFile')
    def test_update_bdu_missing_xml_in_zip(self, mock_zipfile, mock_file, mock_remove, mock_exists, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.iter_content.return_value = [b"chunk"]
        mock_get.return_value = mock_response
        mock_exists.return_value = False
        mock_zip_instance = mock_zipfile.return_value.__enter__.return_value
        mock_zip_instance.namelist.return_value = ["wrong_file.xml"]
        with self.assertRaisesRegex(Exception, "export.xml not found in FSTEC BDU archive"):
            self.fstec.update_bdu()

    @patch('xml.etree.ElementTree.parse')
    @patch('os.path.exists')
    def test_find_vulns_by_cve_id_success(self, mock_exists, mock_parse):
        mock_exists.return_value = True
        
        # Create a mock XML structure
        xml_content = """
        <root>
            <vul>
                <identifier>BDU-123</identifier>
                <name>Test Vuln</name>
                <description>Test Desc</description>
                <vul_status>Active</vul_status>
                <severity>Критический</severity>
                <identifiers>
                    <identifier type="CVE">CVE-2023-1234</identifier>
                </identifiers>
            </vul>
        </root>
        """
        mock_tree = MagicMock()
        mock_tree.getroot.return_value = ET.fromstring(xml_content)
        mock_parse.return_value = mock_tree

        cve_list = [{'osv_id': 'CVE-2023-1234', 'component_id': 1}]
        
        result = self.fstec.find_vulns_by_cve_id(cve_list, 'common')
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['cve_id'], 'CVE-2023-1234')
        self.assertEqual(result[0]['severity'], 'Critical')
        self.assertEqual(result[0]['bdu_id'], 'BDU-123')

    @patch('xml.etree.ElementTree.parse')
    @patch('os.path.exists')
    def test_find_vulns_by_cve_id_no_match(self, mock_exists, mock_parse):
        mock_exists.return_value = True
        xml_content = "<root><vul><identifiers><identifier type='CVE'>CVE-0000</identifier></identifiers></vul></root>"
        mock_tree = MagicMock()
        mock_tree.getroot.return_value = ET.fromstring(xml_content)
        mock_parse.return_value = mock_tree

        cve_list = [{'osv_id': 'CVE-2023-1234', 'component_id': 1}]
        result = self.fstec.find_vulns_by_cve_id(cve_list, 'common')
        self.assertEqual(len(result), 0)

    @patch('app.services.fstec.bdu_fstec.get_vulnerabilities_ids')
    @patch('app.services.fstec.bdu_fstec.get_bdu_vulnerabilities')
    @patch('app.services.fstec.bdu_fstec.add_bdu_vulnerabilities')
    @patch('app.services.fstec.bdu_fstec.FSTEC.find_vulns_by_cve_id')
    def test_update_vulns_adds_new_vulns(self, mock_find, mock_add, mock_get_existing, mock_get_ids):
        mock_get_ids.return_value = [{'osv_id': 'CVE-1', 'component_id': 1}]
        mock_find.return_value = [{
            'component_id': 1, 'component_type': 'common', 'bdu_id': 'B1',
            'cve_id': 'CVE-1', 'name': 'N', 'description': 'D', 'status': 'S',
            'bdu_severity': 'Sev', 'severity': 'Critical'
        }]
        mock_get_existing.return_value = [] # No existing vulns
        
        self.fstec.update_vulns('common')
        
        mock_add.assert_called_once()
        self.assertEqual(len(mock_add.call_args[0][0]), 1)

if __name__ == '__main__':
    unittest.main()
