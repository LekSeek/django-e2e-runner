import logging
import os
import platform
import sys
from multiprocessing import Process

import django
from django.core.management import call_command
from django.test.utils import override_settings
from django.utils.module_loading import import_string

from django_e2e_runner import settings
from django_e2e_runner.utils import wait_net_service


class DjangoTestServer(object):
    def __init__(self, use_threading=False, verbose=False, address=settings.SERVER_IP, port=settings.SERVER_PORT):
        self.address = address
        self.port = port
        self.use_threading = use_threading
        self.server_process = None
        self.verbose = verbose

    @property
    def addrport(self):
        return '{}:{}'.format(self.address, str(self.port))

    def start(self):
        self.server_process = Process(
            target=runserver_wrapper,
            kwargs={
                'verbose': self.verbose,
                'addrport': self.addrport,
                'use_threading': self.use_threading,
            },
        )

        self.server_process.start()

        if not wait_net_service(self.address, self.port, timeout=30):
            self.terminate()
            return False

        return True

    def terminate(self):
        if self.server_process.is_alive():
            self.server_process.terminate()


# Windows compatibility: this function must be defined at the top level of
# a module. On Windows all arguments (including `target` function)
# of Process.__init__  must be picklable.
def runserver_wrapper(addrport, use_threading, verbose=True):
    django.setup()  # (required on Windows)

    if not verbose:
        f = open(os.devnull, 'w')
        sys.stdout = f
        sys.stderr = f

        logging_config = {
            'handlers': {
                'h': {
                    'class': 'logging.NullHandler',
                },
            },
            'loggers': {
                '': {
                    'handlers': ['h'],
                },
            },
            'version': 1,
        }
        logging.config.dictConfig(logging_config)

    with override_settings(ROOT_URLCONF='django_e2e_runner.urls',
                           ORIG_ROOT_URLCONF=settings.ROOT_URLCONF):
        db_class = import_string(settings.DATABASE_CLASS)

        if platform.system() == 'Windows':
            db_class.connect_to_test_database()

        use_threading = use_threading \
            and db_class.allows_multiple_connections()

        call_command(
            'runserver',
            addrport=addrport,
            # TODO allow use_reloader=True, one possible solution might
            # be to wrap all the code (from run_tests.py) before and after
            # the server setup in a `if os.environ.get('RUN_MAIN', False):`
            # See: https://code.djangoproject.com/ticket/8085
            # https://chase-seibert.github.io/blog/2013/10/24/django-subclass-runserver.html
            # https://stackoverflow.com/questions/28489863/why-is-run-called-twice-in-the-django-dev-server
            use_reloader=False,
            use_threading=use_threading,
        )
