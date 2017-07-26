from django.conf import settings


def get_relative_path_to_media(path):
    media_root = settings.MEDIA_ROOT
    relative_path = path.replace(media_root+'/', '')
    return relative_path
