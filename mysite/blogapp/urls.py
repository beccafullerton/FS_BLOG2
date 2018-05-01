from django.urls import include, path, re_path
from django.contrib import admin
from . import views

app_name = 'blogapp'
urlpatterns = [
	# project homepage, ex: /blog/
	path('', views.blogHome, name='blogHome'),
]

urlpatterns += [
	# page to create an account
	path('accounts/new_account/', views.CreateAccountView.as_view(), name='create_account'),
	re_path(r'^profile/$', views.UserProfileView.as_view(), name='user_profile'),
]

urlpatterns += [
	re_path(r'^posts$', views.getPosts, name='get_posts'),
	path('post_list/', views.postList.as_view(), name='post_list'),
	path('create_post/', views.BlogPostCreate.as_view(), name='create_post'),
	path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
	path('post/<int:pk>/edit/', views.BlogPostEdit.as_view(), name='edit_post'),
	path('post/<int:pk>/delete/', views.BlogPostDelete.as_view(), name='delete_post'),
# 	path('<author>/profile/', views.AuthorView.as_view(), name='author_profile'),
]

