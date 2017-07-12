from django.template import loader, Context

__author__ = 'Sohel'

class TemplateLoader(object):

    @classmethod
    def load_template(cls, template_name, context={}):
        try:
            template = loader.get_template(template_name)
            cntxt = Context(context)
            return template.render(cntxt)
        except Exception as exp:
            print("No Template Found")