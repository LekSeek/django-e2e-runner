from django.utils.module_loading import import_string


class ScriptFixtureLoader(object):
    def load(self, fixture_name):
        fixture_method = import_string('tests.fixtures.{}'.format(fixture_name))
        return fixture_method()
