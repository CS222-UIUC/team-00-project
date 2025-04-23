from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class LoggedInUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class UserTextData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    text_data = models.TextField()

    def __str__(self):
        return f"{self.user.username}'s text data"
