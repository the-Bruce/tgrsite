from django.core.management.base import BaseCommand, CommandError
from gallery.models import GalleryImage

from django.contrib.staticfiles import finders
from os import listdir
from os.path import isfile, join

# Adds images from gallery_photos to gallery that aren't already there
class Command(BaseCommand):
	help = 'Creates gallery'

	def handle(self, *args, **options):
		# resolves the full local path of static files
		gallery_dir = finders.find('gallery_photos/') or "None"


		images = [
			# every file in the gallery directory
			f for f in listdir(gallery_dir)
			if isfile(join(gallery_dir, f))

			# that doesn't have an image already
			and not GalleryImage.objects.filter(filename=f).exists()
		]

		for f in images:
			i = GalleryImage.objects.create(filename=f, caption="No caption")
			self.stdout.write('Added {} to gallery'.format(f))

		self.stdout.write('All done!')
