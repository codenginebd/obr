from django.db import transaction
from generics.libs.loader.loader import load_model
from logger.models.error_log import ErrorLog


class CategoryUploader(object):
    def __init__(self, data=[], *args, **kwargs):
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def handle_upload(self):
        ProductCategory = load_model(app_label="ecommerce", model_name="ProductCategory")
        try:
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
                        ErrorLog.log(url='', stacktrace='Category name is missing. Data %s' % str(row),
                                     context=ProductCategory.__name__)
                        continue

                    try:
                        if not show_name_2:
                            show_name_2 = 0
                        show_name_2 = int(show_name_2)
                        if show_name_2 == 1:
                            if not category_name_2:
                                ErrorLog.log(url='', stacktrace='Category name 2 missing. Data: %s skipping...' % row,
                                             context=ProductCategory.__name__)
                                continue
                    except Exception as exp:
                        ErrorLog.log(url='', stacktrace='Show name 2 must be number. Given %s. skipping...' % show_name_2,
                                     context=ProductCategory.__name__)
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
                                    ErrorLog.log(url='',
                                                 stacktrace="Parent category doesn't exist. Skipping... Data: %s" % str(row),
                                                 context=ProductCategory.__name__)
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
                            ErrorLog.log(url='',
                                         stacktrace="Invalid Category Code. Skipping... Data: %s" % str(row),
                                         context=ProductCategory.__name__)
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
                                    ErrorLog.log(url='',
                                                 stacktrace="Parent category doesn't exist. Skipping... Data: %s" % str(row),
                                                 context=ProductCategory.__name__)
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
                                    ErrorLog.log(url='',
                                                 stacktrace="Parent category doesn't exist. Skipping... Data: %s" % str(row),
                                                 context=ProductCategory.__name__)
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
            return True
        except Exception as exp:
            ErrorLog.log(url='',
                         stacktrace="Exception Occured. Message: %s" % str(exp),
                         context=ProductCategory.__name__)
            return False
