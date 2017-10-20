from django.conf import settings


def get_relative_path_to_media(path):
    media_root = settings.MEDIA_ROOT
    relative_path = path.replace(media_root+'/', '')
    return relative_path


def merge_dict(*d):
    merged_dict = {}
    for each in d:
        if type(each) is dict:
            for key, item in each.items():
                merged_dict[key] = item
    return merged_dict


def get_tz_from_request(request):
    return settings.DEFAULT_FALLBACK_TZ
