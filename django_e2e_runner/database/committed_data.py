from django.core.management import call_command
from django.db import DEFAULT_DB_ALIAS, connections

from django_e2e_runner.database.base import BaseDataManager


class CommittedData(BaseDataManager):
    """Load fixtures as committed data and reset with a full flush.

    Unlike ``GlobalTransaction`` -- which loads fixtures inside an uncommitted
    transaction and is therefore visible to a single connection only -- this
    manager commits the fixture data so that every connection sees it. That is
    what allows the test server to run with multiple workers
    (``THREADED_SERVER``), like production.

    State is reset by flushing the database *before* each load rather than after
    the spec: the reset that matters is the one that guarantees a clean database
    at load time, and doing it before the load also self-heals if a previous
    spec crashed without rolling back.
    """

    def _flush(self):
        connection = connections[DEFAULT_DB_ALIAS]
        if not connection.get_autocommit():
            connection.set_autocommit(True)
        call_command(
            'flush',
            verbosity=0,
            interactive=False,
            database=DEFAULT_DB_ALIAS,
            allow_cascade=True,
        )

    def pre_load_setup(self, clear_previous=True):
        if clear_previous:
            self._flush()

    def rollback(self):
        # No-op: clear-before-load in pre_load_setup already guarantees a clean
        # database for the next load, so a post-spec flush would be redundant.
        # The rollback endpoint still calls this; it simply has nothing to do.
        pass
