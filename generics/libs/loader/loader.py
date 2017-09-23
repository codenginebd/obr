from django.apps import apps


def load_model(app_label, model_name):
    try:
        return apps.get_model(app_label=app_label, model_name=model_name)
    except:
        return None