
import copy
import os
import re

from django.core.management.base import BaseCommand

from config.settings.br_apps import BR_APPS

PROJECT_PATH = os.path.abspath(".")


class Command(BaseCommand):
    ignores = ['migrations', 'management', 'static', 'templates', '__pycache__', 'contracts', 'managers', 'generics', 'static', 'templates','static_media']
    cascades = ['models', 'views', 'forms', 'reports']
    ignore_files = ['translation.py', 'urls.py', 'settings.py', 'manage.py']
    _c = [
        re.compile('^class(\s)+(?P<classname>(\w)+)\([a-zA-Z0-9_.]*(,(\s)*([a-zA-Z0-9_.])+)*\)')
        # ,re.compile('^def(\s)+(?P<classname>(\w)+)\([a-zA-Z0-9_.]*(,(\s)*([a-zA-Z0-9_.])+)*\)')
    ]
    _n_c = re.compile('(\s)*class(\s)+Meta')

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.requires_system_checks = False
        self.can_import_settings = False
        self.leave_locale_alone = True

    def validate(self, app=None, display_num_errors=False):
        return False

    def add_argument(self, parser):
        parser.add_argument('--clean',
                            action='store_true',
                            dest='clean',
                            default=False,
                            help='Clean files only')

    def is_matched(self, path, items):
        _p = path.replace(PROJECT_PATH + os.sep, '')
        _f = list(
            filter(lambda a: re.search((os.path.normpath(a) + os.sep).replace('\\', '\\\\') + '(.+)', _p) is not None,
                   items))
        return len(_f) > 0

    def clear_files(self, path, **options):
        if self.is_matched(path, self.ignores):
            return

        n_path = os.path.join(path, '__init__.py')
        self.clear_file(n_path)

        for f in filter(lambda a: os.path.isdir(os.path.join(path, a)) and a != '__pycache__', os.listdir(path)):
            if self.is_matched(os.path.join(path, f), self.cascades) or options.get('cascade', False):
                opts = copy.deepcopy(options)
                opts.update({
                    'cascade': True
                })
                self.clear_files(os.path.join(path, f), **opts)
            else:
                self.clear_files(os.path.join(path, f), **options)

    def generate_files(self, path, top=False, **options):
        if self.is_matched(path, self.ignores):
            return [[], []]

        imports = list()
        all_classes = dict()

        n_path = os.path.join(path, '__init__.py')
        # self.clear_file(n_path)

        for f in filter(lambda a: os.path.isdir(os.path.join(path, a)) and a != '__pycache__', os.listdir(path)):
            if self.is_matched(os.path.join(path, f), self.cascades) or options.get('cascade', False):
                opts = copy.deepcopy(options)
                opts.update({
                    'cascade': True
                })
                values = self.generate_files(os.path.join(path, f), top=False, **opts)
                imports += values[0]
                all_classes.update(values[1])
            else:
                values = self.generate_files(os.path.join(path, f), **options)

        if 'clean' in options and options['clean']:
            self.stdout.write(n_path.replace(PROJECT_PATH + os.sep, '') + "  ...  cleaned")
            return [[], []]

        for f in filter(lambda a: not os.path.isdir(a), os.listdir(path)):
            if f.endswith(".py") and f != '__init__.py' and f[-4:] != '.pyc' and not self.is_matched(
                    os.path.join(path, f), self.ignores):
                if f.replace(path, '') in self.ignore_files:
                    continue
                _path = os.path.join(path, f)
                with open(_path) as _file:
                    try:
                        for line in _file:
                            for c in self._c:
                                result = c.search(line)
                                if result is not None and self._n_c.search(line) is None:
                                    _imp = os.path.join(path, f[:-3]).replace(PROJECT_PATH + os.sep, '').replace(os.sep,
                                                                                                                 '.')
                                    if _imp not in imports:
                                        all_classes[_imp] = []
                                        imports.append(_imp)
                                    all_classes[_imp].append(result.group('classname'))
                        _file.close()
                    except Exception as exp:
                        self.stdout.write(str(exp))
                        _file.close()
        if not top and len(imports) > 0 and not options.get('cascade', False):
            self.stdout.write(
                n_path.replace(PROJECT_PATH + os.sep, '') + " ... " + str(len(all_classes)) + " classes added.")
            self.write_imports(n_path, imports, all_classes)
            self.write_classes(n_path, all_classes)
        return [imports, all_classes]

    def clear_file(self, path):
        _f = open(path, 'w+')
        _f.write('__author__ = "auto generated"\n\n')
        _f.close()

    def write_imports(self, path, imports, classes):
        _f = open(path, 'a')
        for _i in imports:
            _f.write("from " + _i + " import ")
            i = 0
            for _j in classes[_i]:
                if i > 0:
                    _f.write(', ')
                _f.write(_j)
                i += 1
            _f.write("\n")
        _f.write('\n\n')
        _f.close()

    def write_classes(self, path, classes):
        _f = open(path, 'a')
        i = 0
        for _i in classes:
            for _j in classes[_i]:
                if i == 0:
                    _f.write('__all__ = [\'' + _j + '\']\n')
                else:
                    _f.write('__all__ += [\'' + _j + '\']\n')
            i += 1
        _f.close()

    def handle(self, *args, **options):
        for x in BR_APPS:
            for p in self.cascades:
                v = os.path.join(x.replace('.', os.sep), p)
                if not os.path.exists(v):
                    os.makedirs(v)
                self.clear_files(os.path.join(PROJECT_PATH, os.path.normpath(v)), top=False, **options)

        for x in BR_APPS:
            for p in self.cascades:
                v = os.path.join(x.replace('.', os.sep), p)
                if not os.path.exists(v):
                    os.makedirs(v)
                self.generate_files(os.path.join(PROJECT_PATH, os.path.normpath(v)), top=False, **options)