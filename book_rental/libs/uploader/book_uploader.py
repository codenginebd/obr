import os
from django.conf import settings
from django.db import transaction
from book_rental.models.author import Author
from book_rental.models.book_publisher import BookPublisher
from book_rental.models.language import BookLanguage
from book_rental.models.sales.book import Book
from ecommerce.models.sales.category import ProductCategory
from ecommerce.models.sales.keyword import TagKeyword
from ecommerce.models.sales.product_images import ProductImage
from generics.libs.utils import get_relative_path_to_media
from logger.models.error_log import ErrorLog


class BookUploader(object):
    def __init__(self, data=[], *args, **kwargs):
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def handle_upload(self):
        self.data = self.data[1:]
        for row in self.data:
            with transaction.atomic():
                try:
                    index = 0
                    code = row[index]

                    index += 1
                    book_title = str(row[index]) if row[index] else None
                    
                    index += 1
                    book_title_2 = str(row[index]) if row[index] else None

                    index += 1
                    sub_title = str(row[index]) if row[index] else None
                    
                    index += 1
                    sub_title_2 = str(row[index]) if row[index] else None

                    index += 1
                    isbn = str(row[index]).replace("'", "") if row[index] else None
                    
                    index += 1
                    isbn13 = str(row[index]).replace("'", "") if row[index] else None

                    index += 1
                    description = str(row[index]) if row[index] else None
                    
                    index += 1
                    description_2 = str(row[index]) if row[index] else None

                    index += 1
                    show_2 = str(row[index]) if row[index] else None

                    index += 1
                    category_codes = str(row[index]) if row[index] else None

                    index += 1
                    edition = str(row[index]) if row[index] else None

                    index += 1
                    total_page = str(row[index]) if row[index] else None

                    index += 1
                    publisher_code = str(row[index]) if row[index] else None

                    index += 1
                    published_date = row[index]

                    index += 1
                    cover_photo = str(row[index]) if row[index] else None

                    index += 1
                    language = str(row[index]) if row[index] else None

                    index += 1
                    keywords = str(row[index]) if row[index] else None

                    if keywords:
                        keywords = keywords.split(',')

                    authors = []

                    index += 1
                    author_codes = row[index]

                    authors = author_codes.split(',')
                    authors = [ str(acode) for acode in authors ]

                    index += 1
                    sale_available = row[index]

                    index += 1
                    rent_available = row[index]

                    # Validate data
                    if any([not item for item in [book_title, sub_title, description, isbn,
                                                  edition, total_page, publisher_code, published_date,
                                                  language, keywords, authors
                                                  ]]):
                        error_log = ErrorLog()
                        error_log.url = ''
                        error_log.stacktrace = 'Book Upload missing data: %s. Skipping...' % str(row)
                        error_log.save()
                        continue
                        
                    if not isbn and not isbn13:
                        error_log = ErrorLog()
                        error_log.url = ''
                        error_log.stacktrace = 'ISBN or ISBN13 must be there. Missing both. Skipping... Data %s' % str(row)
                        error_log.save()
                        continue

                    if len(isbn) != 10:
                        error_log = ErrorLog()
                        error_log.url = ''
                        error_log.stacktrace = 'ISBN number must be 10 digit long. Skipping... Data %s' % str(row)
                        error_log.save()
                        continue
                        
                    if len(isbn13) != 13:
                        error_log = ErrorLog()
                        error_log.url = ''
                        error_log.stacktrace = 'ISBN13 number must be 13 digit long. Skipping... Data %s' % str(row)
                        error_log.save()
                        continue

                    try:
                        if not show_2:
                            show_2 = 0
                            show_2 = int(show_2)
                        if show_2 == 1:
                            if not book_title_2 or not description_2:
                                error_log = ErrorLog()
                                error_log.url = ''
                                error_log.stacktrace = 'Book Title, Description is mandatory. Data: %s skipping...' % row
                                error_log.save()
                                continue
                    except Exception as exp:
                        error_log = ErrorLog()
                        error_log.url = ''
                        error_log.stacktrace = 'show_2 must be number. Given %s. skipping...' % show_2
                        error_log.save()
                        continue

                    try:
                        int(float(edition))
                    except Exception as exp:
                        error_log = ErrorLog()
                        error_log.url = ''
                        error_log.stacktrace = 'Invalid edition. Must be number. Skipping... data: %s' % str(row)
                        error_log.save()
                        continue

                    try:
                        total_page = int(float(total_page))
                    except Exception as exp:
                        error_log = ErrorLog()
                        error_log.url = ''
                        error_log.stacktrace = 'Total page must be number. Skipping... data: %s' % str(row)
                        error_log.save()
                        continue

                    book_languages = BookLanguage.objects.filter(short_name=language)
                    if not book_languages.exists():
                        error_log = ErrorLog()
                        error_log.url = ''
                        error_log.stacktrace = 'Invalid language code given. Skipping... Data: %s' % str(row)
                        error_log.save()
                        continue
                    else:
                        language = book_languages.first().pk

                    try:
                        published_date = published_date.date()
                    except Exception as exp:
                        error_log = ErrorLog()
                        error_log.url = ''
                        error_log.stacktrace = 'Invalid published date format given. Skipping... Data: %s' % str(row)
                        error_log.save()
                        continue

                    cat_ids = []
                    if category_codes:
                        category_codes = category_codes.split(',')
                        # Create Book Object
                        cat_not_found = False
                        category_objects = ProductCategory.objects.filter(code__in=category_codes).values('id','code')
                        for cat_object in category_objects:
                            if not cat_object['code'] in category_codes:
                                cat_not_found = True
                                break
                            else:
                                cat_ids += [ cat_object['id'] ]

                        if cat_not_found:
                            error_log = ErrorLog()
                            error_log.url = ''
                            error_log.stacktrace = 'Invalid category code given. Skipping... Data: %s' % str(row)
                            error_log.save()
                            continue
                    else:
                        error_log = ErrorLog()
                        error_log.url = ''
                        error_log.stacktrace = 'No Category found. Skipping... Data: %s' % str(row)
                        error_log.save()
                        continue

                    publisher_objects = BookPublisher.objects.filter(code=str(publisher_code))
                    if not publisher_objects.exists():
                        error_log = ErrorLog()
                        error_log.url = ''
                        error_log.stacktrace = 'Invalid publisher code given. Data: %s' % str(row)
                        error_log.save()
                        continue
                    publisher_id = publisher_objects.first().pk

                    author_object_list = []
                    if authors:
                        athr_not_found = False
                        for author_code in authors:
                            athr_objects = Author.objects.filter(code=str(author_code.strip()))
                            if not athr_objects.exists():
                                error_log = ErrorLog()
                                error_log.url = ''
                                error_log.stacktrace = 'Invalid author code given. Data: %s' % str(row)
                                error_log.save()
                                athr_not_found = True
                                break

                            author_object_list += [athr_objects.first()]

                        if athr_not_found:
                            error_log = ErrorLog()
                            error_log.url = ''
                            error_log.stacktrace = 'Invalid author code given. Data: %s' % str(row)
                            error_log.save()
                            continue
                    else:
                        error_log = ErrorLog()
                        error_log.url = ''
                        error_log.stacktrace = 'NO author found. Data: %s' % str(row)
                        error_log.save()
                        continue

                    try:
                       sale_available = int(sale_available)
                    except:
                        sale_available = False

                    if sale_available:
                        sale_available = True

                    try:
                        rent_available = int(rent_available)
                    except:
                        rent_available = False

                    if rent_available:
                        rent_available = True

                    keyword_object_list = []

                    for keyword in keywords:
                        keyword_instances = TagKeyword.objects.filter(name=keyword)
                        if keyword_instances.exists():
                            keyword_instance = keyword_instances.first()
                        else:
                            keyword_instance = TagKeyword()
                            keyword_instance.name = keyword
                            keyword_instance.save()

                        keyword_object_list += [keyword_instance]

                    # Check if code given. If given then check if book_edition exists else set book_rental
                    # instance to None
                    if code:
                        book_objects = Book.objects.filter(code=code)
                        if book_objects.exists():
                            book_object = book_objects.first()
                        else:
                            error_log = ErrorLog()
                            error_log.url = ''
                            error_log.stacktrace = 'Invalid code given for book. Skipping.... Data %s' % str(code)
                            error_log.save()
                            continue
                    else:
                        book_objects = Book.objects.filter(title=book_title, isbn=str(isbn))
                        if book_objects.exists():
                            book_object = book_objects.first()
                        else:
                            book_object = Book()

                    book_object.title = str(book_title)
                    book_object.subtitle = str(sub_title)
                    book_object.description = str(description)
                    if show_2:
                        book_object.title_2 = book_title_2
                        book_object.subtitle_2 = sub_title_2
                        book_object.description_2 = description_2
                    book_object.show_2 = True if show_2 else False
                    book_object.sale_available = sale_available
                    book_object.rent_available = rent_available
                    book_object.publish_date = published_date
                    if isbn:
                        book_object.isbn = str(isbn)
                    if isbn13:
                        book_object.isbn13 = str(isbn13)
                    book_object.edition = edition
                    book_object.publisher_id = publisher_id
                    book_object.language_id = language
                    book_object.page_count = total_page
                    book_object.save()

                    # Product Image
                    if cover_photo:
                        book_object.images.all().delete()
                        book_object.images.clear()
                        image_full_path = os.path.join(settings.MEDIA_BOOK_PATH, cover_photo)
                        if os.path.exists(image_full_path):
                            image_name_relative_media = get_relative_path_to_media(image_full_path)
                            product_image = ProductImage()
                            product_image.image.name = image_name_relative_media
                            product_image.save()
                            book_object.images.add(product_image)
                        else:
                            error_log = ErrorLog()
                            error_log.url = ''
                            error_log.stacktrace = 'Product image %s not found...' % cover_photo
                            error_log.save()

                    book_object.tags.clear()

                    book_object.tags.add(*keyword_object_list)

                    book_object.categories.clear()

                    cat_object_list = []
                    for cat_id in cat_ids:
                        cat_obj = ProductCategory.objects.get(pk=cat_id)
                        cat_object_list += [ cat_obj ]

                    book_object.categories.add(*cat_object_list)

                    book_object.authors.clear()

                    book_object.authors.add(*author_object_list)

                    print("Done!")
                except Exception as exp:
                    print("Exception Occured")
                    print(str(exp))






            
            
            
            
              
             
            
            

            
            
            