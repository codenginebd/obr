from bauth.models.country import Country
from book.libs.uploader.uploader import Uploader
from book.models.currency import Currency
from book.models.language import Language
from logger.models.error_log import ErrorLog
from engine.exceptions.br_exception import BRException


class CountryLanCountryUploader(Uploader):
    def __init__(self, data=[], *args, **kwargs):
        self.data = data
        self.args = args
        self.kwargs = kwargs

    def data_as_list(self):
        if not self.data:
            raise BRException("No data found")

        currency_list, lan_list = [], []

        for entry in self.data:
            for c in entry['currencies']:
                currency_list += [[ entry['name'], entry['alpha2Code'], entry['alpha3Code'], c ]]
            for l in entry['languages']:
                lan_list += [[entry['name'], entry['alpha2Code'], entry['alpha3Code'], l]]
        data_list = [
            currency_list,
            lan_list
        ]
        return data_list

    def handle_upload(self):

        print("Started...")

        self.data = self.data_as_list()

        currency_list = self.data[0]

        lan_list = self.data[1]

        for row in currency_list:

            country_objects = Country.objects.filter(name=row[0], short_name2=row[1], short_name3=row[2])
            if not country_objects.exists():
                error_log = ErrorLog()
                error_log.url = ''
                error_log.stacktrace = 'Country doesn\'t exist. Data: %s' % row
                error_log.save()
                continue
            country_object = country_objects.first()
            currency_objects = Currency.objects.filter(short_name=row[3])
            if not currency_objects:
                error_log = ErrorLog()
                error_log.url = ''
                error_log.stacktrace = 'Currency doesn\'t exist. Data: %s' % row
                error_log.save()
                continue
            currency_object = currency_objects.first()
            currency_object.country_id = country_object.pk
            currency_object.save()

        for row in lan_list:

            country_objects = Country.objects.filter(name=row[0], short_name2=row[1], short_name3=row[2])
            if not country_objects.exists():
                error_log = ErrorLog()
                error_log.url = ''
                error_log.stacktrace = 'Country doesn\'t exist. Data: %s' % row
                error_log.save()
                continue
            country_object = country_objects.first()
            language_objects = Language.objects.filter(short_name=row[3])
            if not language_objects:
                error_log = ErrorLog()
                error_log.url = ''
                error_log.stacktrace = 'language doesn\'t exist. Data: %s' % row
                error_log.save()
                continue
            language_object = language_objects.first()
            language_object.country_id = country_object.pk
            language_object.save()

        print("Ended...")