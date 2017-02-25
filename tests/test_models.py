from unittest import TestCase

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
