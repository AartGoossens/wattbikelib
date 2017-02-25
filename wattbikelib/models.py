from .constants import WATTBIKE_HUB_FILES_BASE_URL
from .exceptions import RideSessionException

class RideSessionResponseModel:
    def __init__(self, data):
        self._validate(data)
        self.sessions = [RideSessionModel(s) for s in data['results']]

    def _validate(self, response):
        sessions = response['results']
        if not len(sessions):
            raise RideSessionException('No results returned')


class RideSessionModel(dict):
    def __init__(self, data):
        super(RideSessionModel, self).__init__(data)

    def get_user_id(self):
        return self['user']['objectId']
    
    def get_session_id(self):
        return self['objectId']
    
    def _build_url(self, extension):
        return WATTBIKE_HUB_FILES_BASE_URL.format(
            user_id=self.get_user_id(),
            session_id=self.get_session_id(),
            extension=extension)

    def get_tcx_url(self):
        return self._build_url('tcx')

    def get_wbs_url(self):
        return self._build_url('wbs')

    def get_wbsr_url(self):
        return self._build_url('wbsr')
