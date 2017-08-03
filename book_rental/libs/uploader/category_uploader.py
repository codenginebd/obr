from django.db import transaction
# from brlogger.models.error_log import ErrorLog
from generics.models.sales.category import ProductCategory


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
                parent_name = row[index] if row[index] else None
                
                if not category_name:
                    error_log = ErrorLog()
                    error_log.url = ''
                    error_log.stacktrace = 'Category name is missing. Data %s' % str(row)
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
                                parent_category = ProductCategory()
                                parent_category.name = parent_name
                                parent_category.save()

                            category_object.name = category_name
                            category_object.parent_id = parent_category.pk
                            category_object.save()

                        else:
                            category_object.name = category_name
                            category_object.parent_id = None
                            category_object.save()

                    else:
                        continue
                        # error_log = ErrorLog()
                        # error_log.url = ''
                        # error_log.stacktrace = 'Invalid code given. Data %s' % str(row)
                        # error_log.save()
                        # continue
                else:

                    book_category_objects = ProductCategory.objects.filter(name=category_name)
                    if book_category_objects.exists():
                        category_object = book_category_objects.first()
                        if not parent_name:
                            category_object.parent_id = None
                            category_object.save()
                        else:
                            parent_categories = ProductCategory.objects.filter(name=parent_name)
                            if parent_categories.exists():
                                parent_category = parent_categories.first()
                            else:
                                parent_category = ProductCategory()
                                parent_category.name = parent_name
                                parent_category.save()

                            category_object.parent_id = parent_category.pk
                            category_object.save()
                    else:
                        category_object = ProductCategory()
                        if parent_name:
                            parent_categories = ProductCategory.objects.filter(name=parent_name)
                            if parent_categories.exists():
                                parent_category = parent_categories.first()
                            else:
                                parent_category = ProductCategory()
                                parent_category.name = parent_name
                                parent_category.save()

                            category_object.name = category_name
                            category_object.parent_id = parent_category.pk
                            category_object.save()

                        else:
                            category_object.name = category_name
                            category_object.save()
                