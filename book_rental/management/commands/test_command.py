from io import StringIO
from PIL import Image
import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Upload Initialized")
        print("Now")
        f = open('/home/codenginebd/Desktop/online-book-rental/media/author/author1.jpg',encoding='latin1')
        img_data = f.read()
        f.close()
        img = Image.open('/home/codenginebd/Desktop/online-book-rental/media/author/author1.jpg')

        print("Upload done!")