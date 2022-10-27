from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.log_in, name="login"),
    path("logout/", views.log_out, name="logout"),
    path("changepassword/", views.changepassword, name="changepassword"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:user_pk>/follow", views.follow, name="follow"),
]
