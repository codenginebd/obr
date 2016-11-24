class BookUploader(object):
    def __init__(self, data=[], *args, **kwargs):
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def handle_upload(self):
        for row in self.data:
            index = 0
            code = row[index].strip() if row[index] else None
            index += 1
            category_name = row[index] if row[index] else None
            index += 1
            parent_name = row[index] if row[index] else None
            
            if code:
                pass