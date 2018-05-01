from django import forms
from django.forms import ModelForm, widgets, Textarea

from blogapp.models import *

from django.contrib import messages
from django.core.exceptions import NON_FIELD_ERRORS
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.utils.translation import gettext_lazy as _


class CreateUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	
	class Meta:
		model = User
		fields = ('username','email','password1','password2')
		
	def save(self, commit=True):
		user = super(CreateUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.save()
		
		user_id = user.id
		author = Author.objects.create(user=user, name=user.username)
		
		return user
        	
class CreatePostForm(ModelForm):
	
	def __init__(self, *args, **kwargs):
		super(CreatePostForm, self).__init__(*args, **kwargs)
		self.fields['title'].widget.attrs = {
			'class': 'title_entry'
		}
		self.fields['content'].widget.attrs = {
			'class': 'post_content_entry'
		}
	
	class Meta:
		model = BlogPost
		fields = ('title','content')
		
	        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        