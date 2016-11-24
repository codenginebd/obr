from book.models.book_edition import BookEdition
from br_blogger.models.error_log import ErrorLog

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
                error_log.stacktrace = 'Missing data: ' % str(row)
                error_log.save()
                continue
                
            
                
            
            # Create Book Object
            
            
              
             
            
            

            
            
            