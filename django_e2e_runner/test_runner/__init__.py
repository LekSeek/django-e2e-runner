from django.utils.module_loading import import_string

from django_e2e_runner import settings


__all__ = [
    'start_test_runner',
]


def start_test_runner(runner_args, runner_in_docker=False, docker_image=None):
    test_runner_class = import_string(settings.E2E_TEST_RUNNER_CLASS)
    test_runner = test_runner_class()
    return test_runner.start(runner_args, runner_in_docker, docker_image)
