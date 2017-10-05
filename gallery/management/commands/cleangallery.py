from django.core.management.base import BaseCommand, CommandError
from gallery.models import GalleryImage

from django.contrib.staticfiles import finders
from os import listdir
from os.path import isfile, join

# Removes 404d images from gallery.
class Command(BaseCommand):
	help = 'Creates gallery'

	def handle(self, *args, **options):
		# resolves the full local path of static files
		gallery_dir = finders.find('gallery_photos/') or "None"

		for x in GalleryImage.objects.all():
			if not isfile(join(gallery_dir, x.filename)):
				self.stdout.write('Removing {} from gallery'.format(x.filename))
				x.delete()

		self.stdout.write('All done!')
