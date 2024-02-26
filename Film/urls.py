from django.urls import path
from . import views

urlpatterns = [
    path('', views.FilmHome.as_view(), name='home'),
    path('recommendations/', views.FilmRec.as_view(), name='recommendations'),
    path('add_page/', views.AddPage.as_view(), name='add_page'),
    path('media/', views.contact, name='media'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', views.FilmCategory.as_view(), name='category'),
    path('blogpost-like/<slug:blog_slug>/', views.BlogPostLike, name="blogpost_like"),
]