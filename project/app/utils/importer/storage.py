"""
Temporary storage utils

Temporary storage when user uploads a file.

Note: This util is for import table feature only.
If you want to use it, copy it to your folder.

- get_temp_file_name
- get_temp_file_path
- is_valid_file_name
- file_path_to_file_name
- file_name_to_file_path
"""

import os
import re
import uuid
from django.conf import settings


UPLOADS_ROOT = getattr(settings, "UPLOADS_ROOT", None)

if UPLOADS_ROOT is None:
    raise Exception("UPLOADS_ROOT is not defined in settings.py")
else:
    os.makedirs(UPLOADS_ROOT, exist_ok=True)


def get_temp_file_name(prefix='', suffix=''):
    return prefix + str(uuid.uuid4()) + suffix


def get_temp_file_path(*args, **kwargs):
    return os.path.join(UPLOADS_ROOT, get_temp_file_name(*args, **kwargs))


# For security reason, never use file path from user input.
# Use file name instead.
# File name must only contain alpha-numeric characters.

def is_valid_file_name(file_name):
    return re.match(r'^[A-Za-z0-9-\.]+$', file_name) and '..' not in file_name


def file_path_to_file_name(file_path):
    return os.path.basename(file_path)


def file_name_to_file_path(file_name):
    if is_valid_file_name(file_name):
        return os.path.join(UPLOADS_ROOT, file_name)
    else:
        raise Exception("Invalid file name {}".format(file_name))
