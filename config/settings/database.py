__author__ = 'codengine'

DATABASES_CONFIG = {
    'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'book_rental',
            'USER': 'root',
            'PASSWORD': 'root',
            'HOST': '127.0.0.1',
            'PORT': '',
            'OPTIONS': {
                 "init_command": "SET foreign_key_checks = 0;",
            }
        }
}