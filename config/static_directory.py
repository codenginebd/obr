import os
PROJECT_ROOT = os.path.abspath(os.path.dirname(__name__))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'
STATIC_FILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)