from datetime import datetime

from decimal import Decimal

from book.models.author import Author
from book.models.book import Book
from book.models.book_edition import BookEdition

from book.models.book_publisher import BookPublisher
from book.models.category import BookCategory
from book.models.currency import Currency
from book.models.keyword import TagKeyword
from book.models.language import Language
from brlogger.models.error_log import ErrorLog
from engine.clock.Clock import Clock


class BookUploader(object):
    def __init__(self, data=[], *args, **kwargs):
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def handle_upload(self):
        for row in self.data:
          
            index = 0
            code = row[index]
            
            index += 1
            book_title = row[index]
            
            index += 1
            sub_title = row[index]
            
            index += 1
            isbn = row[index]
            
            index += 1
            description = row[index]
            
            index += 1
            category_name = row[index]

            index += 1
            edition = row[index]

            index += 1
            total_page = row[index]

            index += 1
            publisher_name = row[index]

            index += 1
            publisher_description = row[index]

            index += 1
            published_date = row[index]

            index += 1
            total_items = row[index]

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
            
            authors = []
            
            index += 1
            author_name = row[index]

            index += 1
            author_description = row[index]
            
            authors += [
                {
                    "name": author_name,
                    "description": author_description
                }
            ]
            
            while index < len(row):
                author_name = row[index]
                index += 1
                author_description = row[index]
                index += 1
              
                authors += [
                    {
                        "name": author_name,
                        "description": author_description
                    }
                ]
                
            
            # Validate data
            
            # Check if code given. If given then check if book_edition exists else set book instance to None
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
            
            if any( [ not item for item in [ book_title, description, isbn, category_name, 
                                            edition, total_page, publisher_name, published_date, total_items, 
                                            cover_photo, base_price, initial_payable_rent_price, initial_payable_buy_price,
                                            currency_name, language, authors
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
                published_date = Clock(published_date)
            except Exception as exp:
                error_log = ErrorLog()
                error_log.url = ''
                error_log.stacktrace = 'Invalid published date format given. Data: %s' % str(row)
                error_log.save()
                continue
                
                
            # Create Book Object
            category_objects = BookCategory.objects.filter(name=category_name)
            if not category_objects.exists():
                error_log = ErrorLog()
                error_log.url = ''
                error_log.stacktrace = 'Invalid category name given. Data: %s' % str(row)
                error_log.save()
                continue
            category_object = category_objects.first()
                
            if not book_edition_instance:
                book_edition_instance = BookEdition()
                book_edition_instance.isbn = isbn
                
                book_objects = Book.objects.filter(title=book_title, subtitle=sub_title)
                if not book_objects.exists():
                    book_object = Book()
                    book_object.title = book_title
                    book_object.subtitle = sub_title
                    book_object.description = description
                    book_object.category_id = category_object.pk
                    book_object.save()
                    
                else:
                    book_object = book_objects.first()
                    
                book_edition_instance.book_id = book_object.pk
                
                book_edition_instance.edition = edition
                
                book_publisher_objects = BookPublisher.objects.filter(name=publisher_name)
                if book_publisher_objects.exists():
                    book_publisher_object = book_publisher_objects.first()
                else:
                    book_publisher_object = BookPublisher()
                    book_publisher_object.name = publisher_name
                    book_publisher_object.description = publisher_description
                    book_publisher_object.save()
                    
                book_edition_instance.publisher_id = book_publisher_object.pk
                
                book_edition_instance.publish_date = published_date
                
                keyword_object_list = []
                
                for keyword in keywords.split(','):
                    keyword_instances = TagKeyword.objects.filter(name=keyword)
                    if keyword_instances.exists():
                        keyword_instance = keyword_instances.first()
                    else:
                        keyword_instance = TagKeyword()
                        keyword_instance.name = keyword
                        keyword_instance.save()
                        
                    keyword_object_list += [ keyword_instance ]
                    
                language_instance = Language.objects.filter(short_name=language).first()
                
                book_edition_instance.language_id = language_instance.pk
                
                book_edition_instance.page_count = total_page
                
                book_edition_instance.is_used = False
                
                book_edition_instance.save()
                
                book_edition_instance.tags.add(*keyword_object_list)
                
                author_object_list = []
                
                for author in authors:
                    author_objects = Author.objects.filter(name=author['name'])
                    if author_objects.exists():
                        author_object = author_objects.first()
                    else:
                        author_object = Author()
                        author_object.name = author['name']
                        author_object.description = author['description']
                        author_object.save()
                    
                    author_object_list += [ author_object ]
                    
                book_edition_instance.authors.add(*author_object_list)
                
            else:
                book_object = book_edition_instance.book
                book_object.title = book_title
                book_object.subtitle = sub_title
                book_object.description = description
                book_object.save()
                
                book_edition_instance.edition = edition
                
                book_publisher_object = book_edition_instance.publisher
                book_publisher_object.name = publisher_name
                book_publisher_object.description = publisher_description
                book_publisher_object.save()
                
                book_edition_instance.publish_date = published_date
                
                keyword_object_list = []
                
                for keyword in keywords.split(','):
                    keyword_instances = TagKeyword.objects.filter(name=keyword)
                    if keyword_instances.exists():
                        keyword_instance = keyword_instances.first()
                    else:
                        keyword_instance = TagKeyword()
                        keyword_instance.name = keyword
                        keyword_instance.save()
                        
                    keyword_object_list += [ keyword_instance ]
                    
                language_instance = Language.objects.filter(short_name=language).first()
                
                book_edition_instance.language_id = language_instance.pk
                
                book_edition_instance.page_count = total_page
                
                book_edition_instance.save()
                
                book_edition_instance.tags.clear()
                
                book_edition_instance.tags.add(*keyword_object_list)
                
                author_object_list = []
                
                for author in authors:
                    author_objects = Author.objects.filter(name=author['name'])
                    if author_objects.exists():
                        author_object = author_objects.first()
                    else:
                        author_object = Author()
                        author_object.name = author['name']
                        author_object.description = author['description']
                        author_object.save()
                    
                    author_object_list += [ author_object ]
                    
                book_edition_instance.authors.clear()
                    
                book_edition_instance.authors.add(*author_object_list)
                
            
            
            
            
              
             
            
            

            
            
            