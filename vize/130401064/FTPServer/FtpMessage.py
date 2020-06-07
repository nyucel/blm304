
from json import JSONEncoder


class FtpMessage:

    def __init__(self, session_id, method, credentials=None, data=None, result=None):
        self.protocol = 'FTP'
        self.version = '1.0'
        self.session_id = session_id
        self.method = method
        self.credentials = credentials
        self.data = data
        self.result = result


class FtpCredentials:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class FtpData:
    def __init__(self, data_id, is_last, header=None, content=None):
        self.data_id = data_id
        self.is_last = is_last
        self.header = header
        self.content = content


class FtpResult:
    def __init__(self, code, description):
        self.code = code
        self.description = description


class FtpMessageEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

