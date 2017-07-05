from django.db import transaction
from book.models.category import BookCategory
# from brlogger.models.error_log import ErrorLog


class GEOUploader(object):
    def __init__(self, data=[], *args, **kwargs):
        self.data = data
        self.args = args
        self.kwargs = kwargs

        self.country_list = []
        self.division_list = []
        self.district_list = []
        self.upazilla_list = []

        self.country_dict = {}
        self.division_dict = {}
        self.district_dict = {}
        self.upazilla_dict = {}

    def handle_upload(self):
        for row in self.data:
            country_name = row[0]
            division_name = row[1]
            district_name = row[2]
            upazila_name = row[3]

            if country_name and division_name and district_name and upazila_name:
                if not country_name in self.country_list:
                    self.country_list += [ country_name ]

                if not division_name in self.division_list:
                    self.division_list += [ division_name ]

                if not district_name in self.district_list:
                    self.district_list += [ district_name ]

                if not upazila_name in self.upazilla_list:
                    self.upazilla_list += [ upazila_name ]


                for cname in self.country_list:
                    c_objects = Country.objects.filter(name=country_name)
                    if c_objects.exists():
                        c_object = c_objects.first()
                    else:
                        c_object = Country()
                        c_object.name = cname
                        c_object.save()
                        self.country_dict[cname] = c_object
