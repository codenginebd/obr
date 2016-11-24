from django.db import transaction
from book.models.category import BookCategory

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
                    # Log error
                    continue

                if code:
                    category_objects = BookCategory.objects.filter(code=code)
                    if category_objects.exists():
                        category_object = category_objects.first()

                        if parent_name:
                            parent_categories = BookCategory.objects.filter(name=parent_name)
                            if parent_categories.exists():
                                parent_category = parent_categories.first()
                            else:
                                parent_category = BookCategory()
                                parent_category.name = parent_name
                                parent_category.save()

                            category_object.name = category_name
                            category_object.parent = parent_category.pk
                            category_object.save()

                        else:
                            category_object.name = category_name
                            category_object.parent = None
                            category_object.save()

                    else:
                        pass # Log error
                else:
                    category_object = BookCategory()
                    if parent_name:
                        parent_categories = BookCategory.objects.filter(name=parent_name)
                        if parent_categories.exists():
                            parent_category = parent_categories.first()
                        else:
                            parent_category = BookCategory()
                            parent_category.name = parent_name
                            parent_category.save()

                        category_object.name = category_name
                        category_object.parent = parent_category.pk
                        category_object.save()

                    else:
                        category_object.name = category_name
                        category_object.save()
                