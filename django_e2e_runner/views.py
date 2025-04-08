from django.http import JsonResponse
from django.utils.module_loading import import_string

from django_e2e_runner import settings


STATUS_OK_200 = "OK"


def load_test_data(request, fixture_name):
    data_manager = import_string(settings.TEST_DATA_MANAGER)()
    data_manager.pre_load_setup()

    fixture_loader = import_string(settings.FIXTURE_LOADER)()
    fixture_data = fixture_loader.load(fixture_name)

    return JsonResponse({'status': STATUS_OK_200, 'data': fixture_data})


def rollback_test_data(request):
    data_manager = import_string(settings.TEST_DATA_MANAGER)()
    data_manager.rollback()
    return JsonResponse({'status': STATUS_OK_200})
