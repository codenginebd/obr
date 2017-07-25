from io import StringIO
from PIL import Image

class ThumbnailModelMixin(object):
    def create_thumbnail(self):
        try:
            # original code for this method came from
            # http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/

            # If there is no image associated with this.
            # do not create thumbnail
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
                print("Now!")
                # Open original photo which we want to thumbnail using PIL's Image
                image = Image.open(StringIO(self.image.read()), 'rb')
                # Convert to RGB if necessary
                # Thanks to Limodou on DjangoSnippets.org
                # http://www.djangosnippets.org/snippets/20/
                #
                # I commented this part since it messes up my png files
                #
                #if image.mode not in ('L', 'RGB'):
                #    image = image.convert('RGB')
                # We use our PIL Image object to create the thumbnail, which already
                # has a thumbnail() convenience method that contrains proportions.
                # Additionally, we use Image.ANTIALIAS to make the image look better.
                # Without antialiasing the image pattern artifacts may result.
                image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
                # Save the thumbnail
                temp_handle = StringIO()
                image.save(temp_handle, PIL_TYPE)
                temp_handle.seek(0)

                # Save image to a SimpleUploadedFile which can be saved into
                # ImageField
                suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                     temp_handle.read(), content_type=DJANGO_TYPE)
                # Save SimpleUploadedFile into image field
                self.thumbnail = suf
        except:
            pass

