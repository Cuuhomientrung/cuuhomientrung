from django.conf import settings


def global_params(context):
    return {
        'REVISION': settings.REVISION,
    }
