class WattbikeHubClient:
    def __init__(self):
        pass

    def login(self):
        raise NotImplementedError

    def logout(self):
        raise NotImplementedError

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
