class RideSessionException(Exception):
    def __init__(self, message):
        super(RideSessionException, self).__init__(message)

class SessionIdNotSupportedException(Exception):
    pass
