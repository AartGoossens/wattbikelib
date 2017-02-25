import pandas as pd

from .constants import WATTBIKE_HUB_FILES_BASE_URL
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


class WattbikeDataFrame(pd.DataFrame):
    def __init__(self, *args, **kwargs):
        super(WattbikeDataFrame, self).__init__(*args, **kwargs)
        self.columns_to_numeric()

    @property
    def _constructor(self):
        return WattbikeDataFrame

    def plot_polar_view(self):
        raise NotImplementedError

    def columns_to_numeric(self):
        numeric_columns = set(self.columns) - set(['polar_force'])
        for col in numeric_columns:
            self.ix[:, col] = pd.to_numeric(self.ix[:, col])
