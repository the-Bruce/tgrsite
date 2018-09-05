from django.db import models
from users.models import Member
from django.urls import reverse

class Newsletter(models.Model):
	def __str__(self):
		return self.title

	title = models.CharField(max_length=256)
	body = models.TextField()
	author = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
	pub_date = models.DateTimeField('Date Posted', auto_now_add=True)
	desc = models.CharField('Description', max_length=256)
	ispublished = models.BooleanField('Is Published?')

# Important! If this changes, change the URL too!
	def get_absolute_url(self):
		return reverse('newsletters_detail', kwargs={'pk': self.id})
