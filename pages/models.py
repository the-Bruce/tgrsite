from django.db import models

class Page(models.Model):
	def __str__(self):
		return self.name

	name = models.CharField(max_length=64, blank=False)
	name.help_text='Internal name of page'

	title = models.CharField(max_length=64, blank=True)
	title.help_text='Page title to display in titlebar of browser/tab'

	body = models.TextField(max_length=16384, blank=True)
	body.help_text='Page contents'

	head = models.TextField(max_length=16384, blank=True)
	head.help_text='Custom HTML to go in the <head> of the page'

	css = models.TextField(max_length=16384, blank=True)
	css.help_text='Custom CSS styles for the page'

	leftbar = models.TextField(max_length=16384, blank=True)
	leftbar.help_text='Left sidebar contents (use panels)'
	rightbar = models.TextField(max_length=16384, blank=True)
	rightbar.help_text='Right sidebar contents (use panels)'
