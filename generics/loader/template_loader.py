from django.template import loader, Context

__author__ = 'Sohel'


class TemplateLoader(object):
    @classmethod
    def load_template(cls, template_name, context={}):
        try:
            template = loader.get_template(template_name)
            return template.render(context)
        except Exception as exp:
            pass
