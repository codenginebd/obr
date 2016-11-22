from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Book Initializing...")
        print("Now")