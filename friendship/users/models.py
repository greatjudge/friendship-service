from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    friends = models.ManyToManyField('self',
                                     blank=True,
                                     related_query_name='friend')

    def __str__(self):
        return self.username
