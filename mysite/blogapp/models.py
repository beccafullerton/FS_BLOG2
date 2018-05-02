from django.db import models
from django.db.models.signals import post_save
from django.core.cache import cache
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse

from django.utils import timezone

class Author(models.Model):
	user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, editable=False)
	name = models.CharField(max_length=200)
	
	def __str__(self):
		return self.name
	
	def to_dict(self):
		return {
			'name': self.name,
		}

class BlogPost(models.Model):
	title = models.CharField(max_length=200)
	pub_date = models.DateField(auto_now_add=True)
	pub_time = models.TimeField(auto_now_add=True)
	last_edit_date = models.DateTimeField(auto_now=True)
	author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL, editable=False)
	content = models.TextField(null=True)
	
		
	def __str__(self):
		return self.title
	
	def get_absolute_url(self):
		return reverse('blogapp:blog/post_detail', kwargs={ 'pk' : self.pk })

	def to_dict(self):
		pub_time = str(self.pub_time)
		pub_date = str(self.pub_date)
		last_edit_date = str(self.last_edit_date)
		author = str(self.author)

		return {
			'id': self.id,
			'title': self.title,
			'pub_date': pub_date,
			'pub_time': pub_time,
			'last_edit_date': last_edit_date,
			'author': author,
			'content': self.content
		}
		
	class Meta:
		ordering = ['pub_date', 'pub_time']