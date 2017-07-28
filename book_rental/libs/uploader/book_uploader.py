from book_rental.models.author import Author
from book_rental.models.book_publisher import BookPublisher
from book_rental.models.language import BookLanguage
from book_rental.models.sales.book import Book
from generics.models.sales.category import ProductCategory
from generics.models.sales.keyword import TagKeyword
from logger.models.error_log import ErrorLog


class BookUploader(object):
    def __init__(self, data=[], *args, **kwargs):
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def handle_upload(self):
        for index, row in enumerate(self.data):

            if index == 0:
                continue

            index = 0
            code = row[index]
            
            index += 1
            book_title = row[index]
            
            index += 1
            sub_title = row[index]
            
            index += 1
            isbn = str(int(row[index]))
            
            index += 1
            description = row[index]
            
            index += 1
            category_codes = row[index]

            index += 1
            edition = row[index]

            index += 1
            total_page = row[index]

            index += 1
            publisher_code = row[index]

            index += 1
            published_date = row[index]

            index += 1
            cover_photo = row[index]
            
            index += 1
            language = row[index]
            
            index += 1
            keywords = row[index]

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
                                          cover_photo, language, keywords, authors
                                          ]]):
                error_log = ErrorLog()
                error_log.url = ''
                error_log.stacktrace = 'Book Upload missing data: %s. Skipping...' % str(row)
                error_log.save()
                continue

            if len(isbn) != 10 and len(isbn) != 13:
                error_log = ErrorLog()
                error_log.url = ''
                error_log.stacktrace = 'ISBN number must be 10 or 13 digit long. Skipping... Data %s' % str(row)
                error_log.save()
                continue
                
            try:
                int(edition)
            except Exception as exp:
                error_log = ErrorLog()
                error_log.url = ''
                error_log.stacktrace = 'Invalid edition. Must be number. Skipping... data: %s' % str(row)
                error_log.save()
                continue
                
            try:
                total_page = int(total_page)
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

            author_object_ids = []
            if authors:
                athr_not_found = False
                for author_code in authors:
                    athr_objects = Author.objects.filter(code=str(author_code))
                    if not athr_objects.exists():
                        error_log = ErrorLog()
                        error_log.url = ''
                        error_log.stacktrace = 'Invalid publisher code given. Data: %s' % str(row)
                        error_log.save()
                        athr_not_found = True
                        break

                    author_object_ids += [athr_objects.first().pk]

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

            for keyword in keywords.split(','):
                keyword_instances = TagKeyword.objects.filter(name=keyword)
                if keyword_instances.exists():
                    keyword_instance = keyword_instances.first()
                else:
                    keyword_instance = TagKeyword()
                    keyword_instance.name = keyword
                    keyword_instance.save()

                keyword_object_list += [keyword_instance]

            # Check if code given. If given then check if book_edition exists else set book_rental instance to None
            book_edition_instance = None
            if code:
                book_objects = Book.objects.filter(code=code)
                if book_objects.exists():
                    book_object = book_objects.first()
                else:
                    error_log = ErrorLog()
                    error_log.url = ''
                    error_log.stacktrace = 'Invalid code given for book. Skipping.... Data %s' % str(row)
                    error_log.save()
                    continue
            else:
                book_object = Book()

            book_object.title = str(book_title)
            book_object.subtitle = str(sub_title)
            book_object.description = str(description)
            book_object.sale_available = sale_available
            book_object.rent_available = rent_available
            book_object.publish_date = published_date
            book_object.isbn = str(isbn)
            book_object.edition = edition
            book_object.publisher_id = publisher_id
            book_object.language_id = language
            book_object.page_count = total_page
            book_object.save()

            book_object.tags.clear()

            book_object.tags.add(*keyword_object_list)

            book_object.categories.clear()

            cat_object_list = []
            for cat_id in cat_ids:
                cat_obj = ProductCategory.objects.get(pk=cat_id)
                cat_object_list += [ cat_obj ]

            book_object.categories.add(*cat_object_list)

            print("Done!")






            
            
            
            
              
             
            
            

            
            
            