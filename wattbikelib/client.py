import json
import requests

import params

from .constants import (
    WATTBIKE_HUB_LOGIN_URL, WATTBIKE_HUB_RIDESESSION_URL)
from .exceptions import InvalidSessionException


class WattbikeHubClient:
    def __init__(self):
        # self._session_init()
        self.session_token = None

    def _create_session(self):
        headers = {'Content-Type': 'application/json'}
        session = requests.Session()
        session.headers = headers
        return session

    def _post_request(self, url, payload):
        data = {
            '_method': 'GET',
            '_ApplicationId': 'Gopo4QrWEmTWefKMXjlT6GAN4JqafpvD',
            '_JavaScriptKey': 'p1$h@M10Tkzw#',
            '_ClientVersion': 'js1.6.14',
            '_InstallationId': 'f375bbaa-9514-556a-be57-393849c741eb'}
        if self.session_token:
            data.update(session_token=self.session_token)
        data.update(payload)

        with self._create_session() as session:
            resp = session.post(
                url=url,
                data=json.dumps(data))

        if not resp.ok:
            # Because Wattbike does not understand http status codes
            resp.reason = resp.content
        resp.raise_for_status()

        return resp

    def login(self):
        self.session_token = None
        payload = {
            'username': params.WATTBIKE_HUB_USERNAME,
            'password': params.WATTBIKE_HUB_PASSWORD}

        resp = self._post_request(
            url=WATTBIKE_HUB_LOGIN_URL,
            payload=payload)

        self.session_token = resp.json()['sessionToken']

    def logout(self):
        raise NotImplementedError

    def get_session_details(self, session_url):
        session_id = session_url.split('/')[-1]
        payload = {
            'where': {
                'objectId': session_id}}

        resp = self._post_request(
            url=WATTBIKE_HUB_RIDESESSION_URL,
            payload=payload)

        return resp.json()

    def get_user_id(self, session_url):
        session_details = self.get_session_details(session_url)
        try:
            results = session_details['results'][0]
        except IndexError:
            raise InvalidSessionException
        else:
            return results['user']['objectId']

    def get_user(self):
        raise NotImplementedError

    def get_sessions(self):
        raise NotImplementedError

    def get_session_data(self):
        raise NotImplementedError

    def get_session_revolutions(self):
        raise NotImplementedError

    def get_session_tcx_url(self):
        raise NotImplementedError

    def get_session_wbs_url(self):
        raise NotImplementedError

    def get_session_wbsr_url(self):
        raise NotImplementedError

    def get_user_preferences(self):
        raise NotImplementedError

    def get_user_performance_state(self):
        raise NotImplementedError
