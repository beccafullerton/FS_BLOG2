# resources for browser navigation and webpage rendering
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.html import escape
from django.urls import reverse_lazy, reverse

# views used in this file
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.views.generic.base import TemplateView

# authentication and login resources
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin

# forms used in this file
from blogapp.forms import CreateUserForm, CreatePostForm

# models used in this file
from django.contrib.auth.models import User
from blogapp.models import *

import json




# INDEX  VIEW
# ===========

def blogHome(request):
	
	return render(
		request,
		'index.html',
		{
		}
	)

def getPosts(request):
	format = 'default'
	info_type = ''
	filter_string = None
	posts = []
	posts_json = []
	post_ids = []
	json_return = []
	new_posts = []
	no_new_posts = 0
	
	format = _clean(request, 'format', 'default')
	filter_string = _clean(request, 'filter')
	info_type = _clean(request, 'info_type')

	posts = BlogPost.objects.filter()
	
	if info_type == 'ids':
		for post in posts:
			post_ids.append(post.id)
		json_return = post_ids
	
	if info_type == 'update_ids':
		current_post_ids = request.GET.getlist('current_post_ids[]', [])
		current_post_ids = [json.loads(item) for item in current_post_ids]
		for post in posts:
			post_ids.append(post.id)
		if post_ids == current_post_ids:
			json_return = ['no new posts']
		else:
			for post in posts:
				if post.id not in current_post_ids:
					new_posts.append(post.to_dict())
					no_new_posts += 1
			json_return = no_new_posts
		
	return HttpResponse(
		json.dumps(json_return),
		content_type='application/json'
	 )

def getAuthors(request):
	format = 'default'
	filter_string = None
	authors = []
	authorslist = []
	
	format = _clean(request, 'format', 'default')
	filter_string = _clean(request, 'filter')
	
	authors = Author.objects.all()
		
	for author in authors:
		authorslist.append(
			[
				"<div><a href='javascript:filter(\"author\", " + str(author.id) + ", \"" + author.name + "\");'>" + author.name + "</a></div>"
			]
		)
	
	return HttpResponse(
		json.dumps(authorslist),
		content_type='application/json'
	 )

class postList(ListView):
	model = BlogPost
	template_name = 'blog/post_list.html'
	
	def get_queryset(self):
		qs = super().get_queryset()
		return BlogPost.objects.all().order_by('-pub_date', '-pub_time')
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context

class FilterListView(ListView):
	model = BlogPost
	template_name = 'blog/filter_list.html'
	format = 'default'
	filter_string = None
	filtered_posts = []
	
	def get_queryset(self):
		format = _clean(self.request, 'format', 'default')
		filter_string = _clean(self.request, 'filter')
		
		if filter_string:
			filters = filter_string.split(",")
			for f in filters:
				f_parts = f.split("_")
				if len(f_parts) == 2:
					filter_type = f_parts[0]
					filter_id = f_parts[1]
					if filter_type == "author":
						filtered_posts = BlogPost.objects.filter(author=filter_id)
# 						return BlogPost.objects.filter(author__username__contains=self.kwargs['author']).order_by('-pub_date')
		qs = super(FilterListView, self).get_queryset()
		return filtered_posts.order_by('-pub_date')


# USER ACCOUNT VIEWS
# ==================

class CreateAccountView(View):
	form_class = CreateUserForm
	initial = { 'key' : 'value'}
	template_name = 'registration/new_account.html'
	
	def get(self, request):
		form = self.form_class(initial=self.initial)
		if request.user.is_authenticated:
			#TODO Give user option to logout or return to profile
			return HttpResponse("You are already logged in.")
		return render(request, self.template_name, { 'form' : form })
	
	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponse('Account created. <a class="btn blue_btn" href="/accounts/login/">login</a>')
		else:
			return HttpResponse('An error has occurred. <a class="btn blue_btn" href="/blog/">Home</a>' )

class UserProfileView(LoginRequiredMixin, ListView):
	model = BlogPost
	template_name = 'profile.html'
	
	def get_queryset(self):
		qs = super(UserProfileView, self).get_queryset()
		user=self.request.user
		id = user.id
		return qs.filter(author__user=id).order_by('-pub_date')



# BLOG POST VIEWS
# ===============

class PostDetail(DetailView):
	model = BlogPost

class BlogPostCreate(LoginRequiredMixin, CreateView):
	template_name = 'blog/create_post.html'
	form_class = CreatePostForm
	initial = { 'key' : 'value'}
	
	def get(self, request):
		form = self.form_class(initial=self.initial)
		return render(request, self.template_name, { 'form' : form })
	
	def form_valid(self, form):
		author = Author.objects.get(user_id=self.request.user.id)
		form.instance.author = author
		return super().form_valid(form)
		if form.is_valid():
			form.save()

class BlogPostEdit(LoginRequiredMixin, UpdateView):
	model = BlogPost
	fields = ('title', 'content')
	template_name = 'edit_post.html'
	
	def get_queryset(self):
		qs = super(BlogPostEdit, self).get_queryset()
		return qs.filter(author=self.request.user)
		
	def form_valid(self, form):
		form.instance.last_edit_date = now
		return super().form_valid(form)
		if form.is_valid():
			form.save()
	
class BlogPostDelete(LoginRequiredMixin, DeleteView):
	model = BlogPost
	template_name = 'delete_post.html'
	
	def get_queryset(self):
		qs = super(BlogPostDelete, self).get_queryset()
		return qs.filter(author=self.request.user)
	success_url='/blog/'

def _clean(request, param, default='', method='GET'):
	clean_value = None

	if method == 'GET':
		clean_value = escape(request.GET.get(param, default))
	elif method == 'POST':
		clean_value = escape(request.POST.get(param, default))

	return clean_value
		
		
# RESUME VIEW
# =============


def resume(request):
	return HttpResponseRedirect("../blog/static/blog/Kempe_Resume_2018.pdf")
	
		
		
		
		
		
		
		
