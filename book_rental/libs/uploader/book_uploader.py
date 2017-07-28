from decimal import Decimal

from book_rental.models.author import Author
from book_rental.models.book import Book
from book_rental.models.book_edition import BookEdition
from book_rental.models.book_publisher import BookPublisher
from book_rental.models.category import BookCategory
from book_rental.models.currency import Currency
from book_rental.models.keyword import TagKeyword
from book_rental.models.language import Language
from book_rental.models.sales.book import Book
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
            category_code = row[index]

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
            base_price = row[index]

            index += 1
            initial_payable_rent_price = row[index]
            
            index += 1
            initial_payable_buy_price = row[index]

            index += 1
            currency_name = row[index]
            
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

            # Validate data

            # Check if code given. If given then check if book_edition exists else set book_rental instance to None
            book_edition_instance = None
            if code:
                book_edition_objects = BookEdition.objects.filter(code=code)
                if book_edition_objects.exists():
                    book_edition_instance = book_edition_objects.first()
                else:
                    error_log = ErrorLog()
                    error_log.url = ''
                    error_log.stacktrace = 'Invalid code given. Data %s' % str(row)
                    error_log.save()
                    continue
            
            if any( [ not item for item in [ book_title, sub_title, description, isbn, category_code,
                                            edition, total_page, publisher_code, published_date, total_items,
                                            cover_photo, base_price, initial_payable_rent_price, initial_payable_buy_price,
                                            currency_name, language, keywords, authors
                                           ] ] ):
                error_log = ErrorLog()
                error_log.url = ''
                error_log.stacktrace = 'Missing data: %s' % str(row)
                error_log.save()
                continue

            if len(isbn) != 10 and len(isbn) != 13:
                error_log = ErrorLog()
                error_log.url = ''
                error_log.stacktrace = 'ISBN number must be 10 or 13 digit long. Data %s' % str(row)
                error_log.save()
                continue
                
            try:
                int(edition)
            except Exception as exp:
                error_log = ErrorLog()
                error_log.url = ''
                error_log.stacktrace = 'Invalid edition. Must be number. data: %s' % str(row)
                error_log.save()
                continue
                
            try:
                total_page = int(total_page)
            except Exception as exp:
                error_log = ErrorLog()
                error_log.url = ''
                error_log.stacktrace = 'Total page must be number. data: %s' % str(row)
                error_log.save()
                continue
                
            try:
                total_items = int(total_items)
            except Exception as exp:
                error_log = ErrorLog()
                error_log.url = ''
                error_log.stacktrace = 'Total number of items must be number. data: %s' % str(row)
                error_log.save()
                continue
                
            try:
                base_price = Decimal(base_price)
            except Exception as exp:
                error_log = ErrorLog()
                error_log.url = ''
                error_log.stacktrace = 'Base price must be decimal number. data: %s' % str(row)
                error_log.save()
                continue
                
            try:
                initial_payable_rent_price = Decimal(initial_payable_rent_price)
            except Exception as exp:
                error_log = ErrorLog()
                error_log.url = ''
                error_log.stacktrace = 'Initial payable rent price must be decimal number. data: %s' % str(row)
                error_log.save()
                continue
                
            try:
                initial_payable_buy_price = Decimal(initial_payable_buy_price)
            except Exception as exp:
                error_log = ErrorLog()
                error_log.url = ''
                error_log.stacktrace = 'Initial payable buy price must be decimal number. data: %s' % str(row)
                error_log.save()
                continue
                
            if not Currency.objects.filter(short_name=currency_name).exists():
                error_log = ErrorLog()
                error_log.url = ''
                error_log.stacktrace = 'Invalid currency code given. Data: %s' % str(row)
                error_log.save()
                continue
                
            if not Language.objects.filter(short_name=language).exists():
                error_log = ErrorLog()
                error_log.url = ''
                error_log.stacktrace = 'Invalid language code given. Data: %s' % str(row)
                error_log.save()
                continue
                
            try:
                published_date = published_date.date()
            except Exception as exp:
                error_log = ErrorLog()
                error_log.url = ''
                error_log.stacktrace = 'Invalid published date format given. Data: %s' % str(row)
                error_log.save()
                continue
                
                
            # Create Book Object
            category_objects = BookCategory.objects.filter(code=category_code)
            if not category_objects.exists():
                error_log = ErrorLog()
                error_log.url = ''
                error_log.stacktrace = 'Invalid category code given. Data: %s' % str(row)
                error_log.save()
                continue
            category_object = category_objects.first()

            publisher_objects = BookPublisher.objects.filter(code=publisher_code)
            if not publisher_objects.exists():
                error_log = ErrorLog()
                error_log.url = ''
                error_log.stacktrace = 'Invalid publisher code given. Data: %s' % str(row)
                error_log.save()
                continue
            publisher_object = publisher_objects.first()

            author_object_list = []
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

                author_object_list += [athr_objects.first()]

            if athr_not_found:
                continue

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


            if code:
                book_objects = Book.objects.filter(code=code)
                if book_objects.exists():
                    book_object = book_objects.first()
                else:
                    error_log = ErrorLog()
                    error_log.url = ''
                    error_log.stacktrace = 'Book with code %s not found.' % str(code)
                    error_log.save()
                    continue

            else:
                book_object = Book()

            book_object.title = book_title
            book_object.subtitle = sub_title
            book_object.description = description

            
            
            
            
              
             
            
            

            
            
            