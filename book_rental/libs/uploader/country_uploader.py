from bauth.models.country import Country
from book_rental.libs.uploader.uploader import Uploader
from logger.models.error_log import ErrorLog
from engine.exceptions.br_exception import BRException


class CountryUploader(Uploader):
    def __init__(self, data=[], *args, **kwargs):
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def data_as_list(self):
        if not self.data:
            raise BRException("No data found")

        data_list = []

        for entry in self.data:
            data_list += [[ entry['name'], entry['alpha2Code'], entry['alpha3Code'] ]]
        return data_list

    def handle_upload(self):

        print("Started...")

        self.data = self.data_as_list()

        for row in self.data:

            if len(row) != 3:
                error_log = ErrorLog()
                error_log.url = ''
                error_log.stacktrace = 'Invalid format in country upload'
                error_log.save()
                continue
            country_objects = Country.objects.filter(name=row[0], short_name2=row[1], short_name3=row[2])
            if country_objects.exists():
                country_object = country_objects.first()
            else:
                country_object = Country()
                country_object.name = row[0]
                country_object.short_name2 = row[1]
                country_object.short_name3 = row[2]
            country_object.save()

        print("Ended...")