from django.db import models

from authentication.models import CustomUser


class Bird(models.Model):
    name = models.CharField(max_length=17)
    color = models.CharField(max_length=31)

    def __str__(self):
        return str(self.id)


class BirdSeen(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    bird_id = models.ForeignKey(Bird, on_delete=models.DO_NOTHING)
    saw_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
