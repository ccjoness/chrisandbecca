from django.db import models
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
import os


def image_upload_handler(instance, filename):
    return 'gallery/full/{}'.format(filename)


def thumbnail_image_upload_handler(instance, filename):
    return 'gallery/thumb/{}'.format(filename)


class GalleryImage(models.Model):
    image = models.ImageField(upload_to=image_upload_handler)
    thumbnail = models.ImageField(upload_to=thumbnail_image_upload_handler)
    approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.make_thumbnail():
            raise Exception('Could not create thumbnail - is the file type valid?')
        super().save(*args, **kwargs)

    def make_thumbnail(self):
        """
        Create and save the thumbnail for the image (simple resize with PIL).
        modified from: https://stackoverflow.com/a/23927211
        """
        image = Image.open(self.image)
        image.thumbnail((420, 420), Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        thumb_name = thumb_name.split('/')[-1]
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False  # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True
