from unittest import TestCase

from wattbikelib import tools


class ToolsTest(TestCase):
    def test_flatten(self):
        a = {
            'a': 'a',
            'nested': {
                'b': 'b'}}
        b = tools.flatten(a)
        for key in b.keys():
            self.assertIsInstance(b[key], str)
        self.assertTrue('nested_b' in b)

    def test_build_url(self):
        user_id = 'u-1756bbba7e2a350'
        session_id = '2yBuOvd92C'
        url = tools.build_hub_files_url(user_id, session_id)
        self.assertTrue(url.endswith('u-1756bbba7e2a350_2yBuOvd92C.wbs'))

    def test_build_url_tcx(self):
        user_id = 'u-1756bbba7e2a350'
        session_id = '2yBuOvd92C'
        url = tools.build_hub_files_url(user_id, session_id, 'tcx')
        self.assertTrue(url.endswith('.tcx'))
