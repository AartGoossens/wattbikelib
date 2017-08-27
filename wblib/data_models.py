from .exceptions import RideSessionException
from .tools import build_hub_files_url


class RideSessionResponseModel:
    def __init__(self, data):
        self._validate(data)
        self.sessions = [RideSessionModel(s) for s in data['results']]

    def _validate(self, response):
        sessions = response['results']
        if not len(sessions):
            raise RideSessionException('No results returned')


class RideSessionModel(dict):
    def get_user_id(self):
        return self['user']['objectId']
    
    def get_session_id(self):
        return self['objectId']
    
    def _build_url(self, extension):
        return build_hub_files_url(
            user_id=self.get_user_id(),
            session_id=self.get_session_id(),
            extension=extension)

    def get_tcx_url(self):
        return self._build_url('tcx')

    def get_wbs_url(self):
        return self._build_url('wbs')

    def get_wbsr_url(self):
        return self._build_url('wbsr')


class LoginResponseModel(dict):
    def get_user_id(self):
        return self['objectId']

    def get_session_token(self):
        return self['sessionToken']


class PerformanceStateModel:
    def __init__(self, data):
        self.data = data['results'][0]['performanceState']

    def get_max_minute_power(self):
        return self.data.get('mmp', None)

    def get_max_hr(self):
        return self.data.get('mhr', None)
 
    def get_ftp(self):
        return self.data.get('ftp', None)
