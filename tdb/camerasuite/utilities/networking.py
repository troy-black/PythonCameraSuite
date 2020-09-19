import socket


_hostname = None
_local_ipv4 = None


def get_hostname():
    global _hostname
    if not _hostname:
        _hostname = socket.gethostname()
    return _hostname
    # _local_ipv4 = socket.gethostbyname(self.hostname)
