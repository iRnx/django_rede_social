# models.py

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username


class FriendRequest(models.Model):
    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='friend_requests_sent')
    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='friend_requests_received')
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.from_user.user.username} to {self.to_user.user.username}"
