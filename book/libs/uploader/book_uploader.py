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
            isbn = row[index]
            index += 1
            description = row[index]

            index += 1
            edition = row[index]

            index += 1
            total_page = row[index]

            index += 1
            author_name = row[index]

            index += 1
            author_description = row[index]

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
            initial_payable = row[index]

            index += 1
            currency_name = row[index]

            0