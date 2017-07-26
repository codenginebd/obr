from io import StringIO
from PIL import Image
from django.conf import settings

from generics.libs.utils import get_relative_path_to_media


class ThumbnailModelMixin(object):
    def create_thumbnail(self):
        try:
            if not self.image:
                return
            if self.image.name.endswith("jpg") or self.image.name.endswith("jpeg") or self.image.name.endswith("png"):
                from PIL import Image
                # from cStringIO import StringIO
                from django.core.files.uploadedfile import SimpleUploadedFile
                import os

                # Set our max thumbnail size in a tuple (max width, max height)
                THUMBNAIL_SIZE = (200,200)

                if self.image.name.endswith("jpg") or self.image.name.endswith("jpeg"):
                    DJANGO_TYPE = "image/jpeg"
                elif self.image.name.endswith("png"):
                    DJANGO_TYPE = "image/png"

                if DJANGO_TYPE == 'image/jpeg':
                    PIL_TYPE = 'jpeg'
                    FILE_EXTENSION = 'jpg'
                elif DJANGO_TYPE == 'image/png':
                    PIL_TYPE = 'png'
                    FILE_EXTENSION = 'png'
                # Open original photo which we want to thumbnail using PIL's Image
                image = Image.open(self.image)
                image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
                # Save the thumbnail
                file_name = self.image.name.split('/')[-1:][0]
                image_path = self.image.name[:self.image.name.rindex('/')]
                image_thumb_dir = os.path.join(settings.MEDIA_ROOT, image_path, 'thumbnails', 'thumb_'+file_name)
                image_file_write = open(image_thumb_dir, 'wb')
                image.save(image_file_write, PIL_TYPE)
                image_file_write.close()
                image_name_relative_media = get_relative_path_to_media(image_thumb_dir)
                self.thumbnail.name = image_name_relative_media
        except Exception as ex:
            print("Exp1: " + str(ex))

