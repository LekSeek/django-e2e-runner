from django.utils.module_loading import import_string

from django_e2e_runner import settings
from django_e2e_runner.database.base import BaseDatabase
from django_e2e_runner.database.committed_data import CommittedData
from django_e2e_runner.database.django_test_database import DjangoTestDatabase
from django_e2e_runner.database.global_transaction import GlobalTransaction
from django_e2e_runner.database.loaders import ScriptFixtureLoader

__all__ = [
    'CommittedData', 'DjangoTestDatabase', 'GlobalTransaction',
    'ScriptFixtureLoader', 'setup_database',
]


def setup_database(*args, **kwargs):
    db_class = import_string(settings.DATABASE_CLASS)
    if issubclass(db_class, BaseDatabase):
        db = db_class()
        db.setup(*args, **kwargs)
        return db

    raise TypeError("'DATABASE_CLASS' should be a subclass of "
                    "django_e2e_runner.database.base.BaseDatabase")
