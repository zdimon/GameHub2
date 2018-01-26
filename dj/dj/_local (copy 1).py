# -*- coding: utf-8 -*-
import os
from .settings import BASE_DIR

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'GameHub',
        'USER': 'postgres',
        'PASSWORD': '1q2w3e',
        'HOST': 'localhost',
    }
}