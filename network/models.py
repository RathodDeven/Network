from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField("User",related_name="follower")



class Post(models.Model):
    poster = models.ForeignKey("User",on_delete=models.CASCADE,related_name="posts")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"Posted by {self.poster} at {self.timestamp}"

    def serialize(self):
        return {
            "id":self.id,
            "poster":self.poster,
            "content":self.content,
            "timestamp":self.timestamp,
            "likes":self.likes
        }


    


