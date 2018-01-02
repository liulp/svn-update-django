
class abc:
    def bcd(self):
        self.efg =  123


class linux(object):
    import paramiko
    def __init__(self, hostname, username, password, port):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
    def ssh(self):
        """ 远程执行命令  """
        self.s = paramiko.SSHClient()
        self.s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.s.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)
