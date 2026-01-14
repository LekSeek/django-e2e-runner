import errno
import socket
from time import time as now


def wait_net_service(server, port, timeout=None):
    s = socket.socket()

    if timeout:
        end = now() + timeout

    while True:
        try:
            if timeout:
                next_timeout = end - now()  # time left until the `end`
                if next_timeout < 0:
                    # the `end` checkpoint already reached
                    return False
                else:
                    s.settimeout(next_timeout)

            s.connect((server, port))

        # TODO test on Windows, with different timeouts
        #      https://bugs.python.org/issue5293
        # except socket.timeout:
        #     return False

        except socket.error as err:
            # catch timeout exception from underlying network library
            # this one is different from socket.timeout
            if err.errno != errno.ECONNREFUSED:
                raise
            s = socket.socket()
        else:
            s.close()
            return True


def parse_command_line_bool_arg(arg):
    upper_arg = str(arg).upper()
    if 'TRUE'.startswith(upper_arg):
        return True
    elif 'FALSE'.startswith(upper_arg):
        return False
    else:
        return bool(arg)
