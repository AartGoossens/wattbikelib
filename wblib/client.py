import datetime
import json

import requests

import params

from .constants import WATTBIKE_HUB_LOGIN_URL, WATTBIKE_HUB_RIDESESSION_URL
from .exceptions import RideSessionException
from .models import (LoginResponseModel, RideSessionResponseModel,
                     WattbikeDataFrame)
from .tools import build_hub_files_url, flatten


class WattbikeHubClient:
    def __init__(self):
        self.session_token = None
        self.user_id = None

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
            data.update({'_SessionToken': self.session_token})
        data.update(payload)

        with self._create_session() as session:
            resp = session.post(
                url=url,
                data=json.dumps(data))

        if not resp.ok:
            # Because Wattbike does not understand http status codes
            resp.reason = resp.content
        resp.raise_for_status()

        return resp.json()

    def _get_request_json(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def login(self):
        self.session_token = None
        payload = {
            'username': params.WATTBIKE_HUB_USERNAME,
            'password': params.WATTBIKE_HUB_PASSWORD}

        data = self._post_request(
            url=WATTBIKE_HUB_LOGIN_URL,
            payload=payload)

        login_response = LoginResponseModel(data)
        self.session_token = login_response.get_session_token()
        self.user_id = login_response.get_user_id()

    def logout(self):
        raise NotImplementedError

    def _ride_session_call(self, payload):
        data = self._post_request(
            url=WATTBIKE_HUB_RIDESESSION_URL,
            payload=payload)
        
        session_response = RideSessionResponseModel(data)

        return session_response.sessions

    def _session_id_from_url(self, session_url):
        return session_url.split('/')[-1]

    def get_session(self, session_url):
        session_id = self._session_id_from_url(session_url)
        payload = {
            'where': {
                'objectId': session_id}}
        
        return self._ride_session_call(payload)[0]

    def get_sessions(self, user_id, before=None, after=None):
        if not before:
            before = datetime.datetime.now()
        if not after:
            after = datetime.datetime(2000, 1, 1)
        payload = {
            'where': {
                'user': {
                    '__type': 'Pointer',
                    'className': '_User',
                    'objectId': user_id},
                'startDate': {
                    '$gt': {
                        '__type': 'Date',
                        'iso': after.isoformat()},
                    '$lt': {
                        '__type': 'Date',
                        'iso': before.isoformat()}}}}

        return self._ride_session_call(payload)

    def get_session_ids(self, user_id, before=None, after=None):
        sessions = self.get_sessions(user_id, before, after)

        return [session.get_user_id() for session in sessions]

    def get_user(self):
        raise NotImplementedError

    def get_session_data(self):
        raise NotImplementedError

    def get_session_revolutions(self):
        raise NotImplementedError

    def get_user_preferences(self):
        raise NotImplementedError

    def get_user_performance_state(self):
        raise NotImplementedError

    def get_session_dataframe(self, session_url=None, user_id=None):
        if not user_id:
            if self.user_id:
                user_id = self.user_id
            else:
                user_id = self.get_user_id_from_session_url(session_url)

        session_id = self._session_id_from_url(session_url)
        url = build_hub_files_url(user_id, session_id)
        wbs = self._get_request_json(url)

        wdf = WattbikeDataFrame(
            [flatten(rev) for lap in wbs['laps'] for rev in lap['data']])

        wdf['time'] = wdf.time.cumsum()
        wdf['user_id'] = user_id
        wdf['session_id'] = session_id
        wdf.process()

        return wdf

    def get_user_id_from_session_url(self, session_url):
        session = self.get_session(session_url)
        return session['user']['objectId']
