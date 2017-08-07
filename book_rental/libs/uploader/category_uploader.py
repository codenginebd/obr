from django.db import transaction
# from brlogger.models.error_log import ErrorLog
from generics.models.sales.category import ProductCategory
from logger.models.error_log import ErrorLog


class CategoryUploader(object):
    def __init__(self, data=[], *args, **kwargs):
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def handle_upload(self):
        for row in self.data:
            with transaction.atomic():
                index = 0
                code = row[index].strip() if row[index] else None
                index += 1
                category_name = row[index] if row[index] else None
                index += 1
                category_name_2 = row[index] if row[index] else None
                index += 1
                show_name_2 = row[index] if row[index] else None
                index += 1
                parent_name = row[index] if row[index] else None
                
                if not category_name:
                    error_log = ErrorLog()
                    error_log.url = ''
                    error_log.stacktrace = 'Category name is missing. Data %s' % str(row)
                    error_log.save()
                    continue
                    
                try:
                    if not show_name_2:
                        show_name_2 = 0
                    show_name_2 = int(show_name_2)
                    if show_name_2 == 1:
                        if not category_name_2:
                            error_log = ErrorLog()
                            error_log.url = ''
                            error_log.stacktrace = 'Category name 2 missing. Data: %s skipping...' % row
                            error_log.save()
                            continue
                except Exception as exp:
                    error_log = ErrorLog()
                    error_log.url = ''
                    error_log.stacktrace = 'Show name 2 must be number. Given %s. skipping...' % show_name_2
                    error_log.save()
                    continue

                if code:
                    category_objects = ProductCategory.objects.filter(code=code)
                    if category_objects.exists():
                        category_object = category_objects.first()

                        if parent_name:
                            parent_categories = ProductCategory.objects.filter(name=parent_name)
                            if parent_categories.exists():
                                parent_category = parent_categories.first()
                            else:
                                error_log = ErrorLog()
                                error_log.url = ''
                                error_log.stacktrace = "Parent category doesn't exist. Skipping... Data: %s" % str(row)
                                error_log.save()
                                continue

                            category_object.name = category_name
                            if show_name_2 == 1:
                                category_object.name_2 = category_name_2
                            category_object.show_name_2 = show_name_2
                            category_object.parent_id = parent_category.pk
                            category_object.save()

                        else:
                            category_object.name = category_name
                            if show_name_2 == 1:
                                category_object.name_2 = category_name_2
                            category_object.show_name_2 = show_name_2
                            category_object.parent_id = None
                            category_object.save()

                    else:
                        error_log = ErrorLog()
                        error_log.url = ''
                        error_log.stacktrace = "Invalid Category Code. Skipping... Data: %s" % str(row)
                        error_log.save()
                        continue
                else:

                    book_category_objects = ProductCategory.objects.filter(name=category_name)
                    if book_category_objects.exists():
                        category_object = book_category_objects.first()
                        if parent_name:
                            parent_categories = ProductCategory.objects.filter(name=parent_name)
                            if parent_categories.exists():
                                parent_category = parent_categories.first()
                            else:
                                 error_log = ErrorLog()
                                 error_log.url = ''
                                 error_log.stacktrace = "Parent category doesn't exist. Skipping... Data: %s" % str(row)
                                 error_log.save()
                                 continue
                            category_object.name = category_name
                            if show_name_2 == 1:
                                category_object.name_2 = category_name_2
                            category_object.show_name_2 = show_name_2
                            category_object.parent_id = parent_category.pk
                            category_object.save()
                        else:
                            category_object.name = category_name
                            if show_name_2 == 1:
                                category_object.name_2 = category_name_2
                            category_object.show_name_2 = show_name_2
                            category_object.save()
                    else:
                        category_object = ProductCategory()
                        if parent_name:
                            parent_categories = ProductCategory.objects.filter(name=parent_name)
                            if parent_categories.exists():
                                parent_category = parent_categories.first()
                            else:
                                error_log = ErrorLog()
                                error_log.url = ''
                                error_log.stacktrace = "Parent category doesn't exist. Skipping... Data: %s" % str(row)
                                error_log.save()
                                continue

                            category_object.name = category_name
                            if show_name_2 == 1:
                                category_object.name_2 = category_name_2
                            category_object.show_name_2 = show_name_2
                            category_object.parent_id = parent_category.pk
                            category_object.save()

                        else:
                            category_object.name = category_name
                            if show_name_2 == 1:
                                category_object.name_2 = category_name_2
                            category_object.show_name_2 = show_name_2
                            category_object.save()
                