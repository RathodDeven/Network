
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("allposts",views.allposts,name="allposts"),
    path("user/<int:user_id>",views.user,name="user"),
    path("user/<int:user_id>/unfollow",views.unfollow,name="unfollow"),
    path("user/<int:user_id>/follow",views.follow,name="follow"),
    path("following/<int:user_id>",views.following,name="following"),
    path("post/<int:post_id>",views.post,name="post"),
    path("like/<int:post_id>",views.like,name="like"),
    path("followers/<int:user_id>",views.followers,name="followers"),
    path("followings/<int:user_id>",views.followings,name="followings")
]
