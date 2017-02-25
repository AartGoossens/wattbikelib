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
