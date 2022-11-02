# -*- coding: utf-8 -*-

"""
This is a django-split-settings main file.

For more information read this:
https://github.com/sobolevn/django-split-settings

To change settings file:
`DJANGO_ENV=production python manage.py runserver`
"""
from os import environ

from split_settings.tools import include

from server.settings.components import config

environ.setdefault("DJANGO_ENV", "development")

_ENV = environ["DJANGO_ENV"]

base_settings = [  # pylint: disable=invalid-name
    "components/common.py",
    "components/telegram.py",
    # You can even use glob:
    # 'components/*.py'
    # Select the right env:
    "environments/{0}.py".format(_ENV),
]

# Include settings:
include(*base_settings)
