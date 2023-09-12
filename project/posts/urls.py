from django.urls import path
from posts import views as post_views


urlpatterns = [
    path('', post_views.index, name='index'),
    path('blog/', post_views.blog, name='post_list'),
    path('search/', post_views.search, name='search'),
    path('create/', post_views.post_create, name='post_create'),
    path('post/<id>/', post_views.post, name='post_detail'),

    path('post/<id>/update/', post_views.post_update, name='post_update'),
    path('post/<id>/delete/', post_views.post_delete, name='post_delete'),

    path('comment/<id>/update/', post_views.comment_update, name='comment_update'),
    path('comment/<id>/delete/', post_views.comment_delete, name='comment_delete'),

    path('about-us/', post_views.about, name='about'),
]
