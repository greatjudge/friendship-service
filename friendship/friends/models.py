from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class FriendRequest(models.Model):
    class Status(models.TextChoices):
        CONS = 'CN', 'consideration'
        REJ = 'RJ', 'reject'

    class Meta:
        unique_together = (('user_to', 'user_from'),)

    user_to = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='incoming_requests')
    user_from = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name='outgoing_requests')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.CONS)
