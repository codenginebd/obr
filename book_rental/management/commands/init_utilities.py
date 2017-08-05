from django.core.management.base import BaseCommand
from config.initialize import init_book_languages,init_rent_plans


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Upload Initialized")
        print("Now")
        init_book_languages()
        #init_rent_plans()
        print("Upload done!")


