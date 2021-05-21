from django.db import models
from django.utils import timezone

from accounts.models import User
from mypage.models import Laboratory

# Create your models here.


class ChatMessageBetweenUserAndLab(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_with_lab')
    laboratory = models.ForeignKey(
        Laboratory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='chat_with_user'
    )
    text = models.TextField()
    send_date = models.DateTimeField(verbose_name='message send date', default=timezone.now)

    def __str__(self):
        return self.laboratory.laboratory_name + '--' + self.user.last_name + '-----' + self.text

    class Meta:
        verbose_name = '研究室-ユーザー間のメッセージ'
        verbose_name_plural = '研究室-ユーザー間のメッセージ一覧'


class ChatMessageBetweenUserAndUser(models.Model):
    send_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_sent_for_user')
    receive_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_received_from_user')
    text = models.TextField()
    send_date = models.DateTimeField(verbose_name='message send date', default=timezone.now)

    def __str__(self):
        return self.send_user.last_name + '--' + self.receive_user.last_name + '-----' + self.text

    class Meta:
        verbose_name = 'ユーザー間のメッセージ'
        verbose_name_plural = '研究室-ユーザー間のメッセージ一覧'
