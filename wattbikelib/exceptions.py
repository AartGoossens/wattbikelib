class InvalidSessionException(Exception):
    def __init__(self):
        super(InvalidSessionException, self).__init__('session url is not valid')

