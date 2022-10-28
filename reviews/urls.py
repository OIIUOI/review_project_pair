from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("index/", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<int:pk>/detail/", views.detail, name="detail"),
    path("<int:pk>/update/", views.update, name="update"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/comments/create", views.comments_create, name="comments_create"),
    path(
        "<int:review_pk>/<int:comment_pk>/delete/", views.comments_delete, name="comment_delete"),
    path("<int:pk>/like/", views.like, name="like"),
    path("<int:review_pk>/<int:comment_pk>/update/", 
    views.comment_update, name = 'comment_update'),
]
