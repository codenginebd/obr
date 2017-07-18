from django.core.management.base import BaseCommand

from book_rental.models.category import BookCategory


class Command(BaseCommand):
    def handle(self, *args, **options):
        BookCategory.objects.all().delete()