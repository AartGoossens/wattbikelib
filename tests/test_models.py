from unittest import TestCase

import requests

from wattbikelib import exceptions, models


class RideSessionResponseModelTest(TestCase):
    def test_init(self):
        response_model = models.RideSessionResponseModel({'results': [{}]})
        self.assertEqual(len(response_model.sessions), 1)

    def test_validate(self):
        response_model = models.RideSessionResponseModel({'results': [{}]})
        self.assertIsNone(response_model._validate({'results': [{}]}))

    def test_validate_no_results(self):
        response_model = models.RideSessionResponseModel({'results': [{}]})
        with self.assertRaisesRegex(
                expected_exception=exceptions.RideSessionException,
                expected_regex='No results returned'):
            response_model._validate({'results': []})


class RideSessionModelTest(TestCase):
    def setUp(self):
        session_data = {
            'objectId': '2yBuOvd92C',
            'user': {
                'objectId': 'u-1756bbba7e2a350'}}
        self.session = models.RideSessionModel(session_data)

    def test_init(self):
        session = models.RideSessionModel({})
        self.assertIsInstance(session, models.RideSessionModel)
        self.assertIsInstance(session, dict)

    def test_get_user_id(self):
        user_id = self.session.get_user_id()
        self.assertEqual(user_id, 'u-1756bbba7e2a350')

    def test_get_session_id(self):
        session_id = self.session.get_session_id()
        self.assertEqual(session_id, '2yBuOvd92C')

    def test_build_url(self):
        url = self.session._build_url('bla')
        self.assertEqual(url,
            'https://api.wattbike.com/v2/files/u-1756bbba7e2a350_2yBuOvd92C.bla')

    def test_get_tcx_url(self):
        url = self.session.get_tcx_url()
        self.assertTrue(url.endswith('u-1756bbba7e2a350_2yBuOvd92C.tcx'))

        response = requests.head(url, headers={'Connection':'close'})
        self.assertTrue(response.ok)

    def test_get_wbs_url(self):
        url = self.session.get_wbs_url()
        self.assertTrue(url.endswith('u-1756bbba7e2a350_2yBuOvd92C.wbs'))

        response = requests.head(url, headers={'Connection':'close'})
        self.assertTrue(response.ok)

    def test_get_wbsr_url(self):
        url = self.session.get_wbsr_url()
        self.assertTrue(url.endswith('u-1756bbba7e2a350_2yBuOvd92C.wbsr'))

        response = requests.head(url, headers={'Connection':'close'})
        self.assertTrue(response.ok)
