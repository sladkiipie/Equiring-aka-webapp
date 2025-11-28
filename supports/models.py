import uuid

from django.conf import settings
from django.db import models
from django.db.models import ForeignKey
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser
from model_utils.models import TimeStampedModel, SoftDeletableModel
from django.db.models import Q
from typing import Optional, Any
from users.models import Contracts, User


def user_directory_path(instance, filename):
    return f"user_{instance.uploaded_by.pk}/{filename}"

class SupporTicket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contract = models.ForeignKey(Contracts, related_name='contract', blank=True,on_delete=models.CASCADE)
    responsible_id = models.ForeignKey(User, related_name='supporter', blank=True,on_delete=models.CASCADE)
    asker_id = models.ForeignKey(User, related_name='asker', blank=True,on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

class SupportMessage(models.Model):
    ticket_id = models.UUIDField(ForeignKey(SupporTicket, default=uuid.uuid4, editable=False, on_delete=models.CASCADE))
    message = models.CharField(max_length=255)
    date_message = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

class UploadedFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Uploaded_by",
                                    related_name="+", db_index=True)
    file = models.FileField(verbose_name="File", blank=False, null=False, upload_to=user_directory_path)
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="Uploaded date")

    def __str__(self):
        return self.file.name

class DialogsModel(TimeStampedModel):
    id = models.BigAutoField(primary_key=True, verbose_name="id")
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="User1",
                              related_name="+", db_index=True)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="User2",
                              related_name="+", db_index=True)

    class Meta:
        unique_together = (('user1', 'user2'), ('user2', 'user1'))
        verbose_name = "Dialogs"
        verbose_name_plural = "Dialogs"

    def __str__(self):
        return _("Dialogs beetwen ") + f"{self.user1} {self.user2}"

    @staticmethod
    def dialog_exists(u1: AbstractBaseUser, u2: AbstractBaseUser) -> Optional[Any]:
        return DialogsModel.objects.filter(Q(user1=u1, user2=u2) | Q(user2=u2, user1=u1)).first()

    @staticmethod
    def create_if_not_exists(u1: AbstractBaseUser, u2: AbstractBaseUser): # Попробовать указать модель User если не будет рабоать
        res = DialogsModel.dialog_exists(u1, u2)
        if not res:
            DialogsModel.objects.create(user1=u1, user2=u2)

    @staticmethod
    def get_diaogs_for_user(user: AbstractBaseUser): # Попробовать указать модель User если не будет рабоать
        return DialogsModel.objects.filter(Q(user1=user) | Q(user2=user)).values_list('user1_pk', 'user2_pk')

class MessageModel(TimeStampedModel, SoftDeletableModel):
    id = models.BigAutoField(primary_key=True, verbose_name="id")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Author",
                               related_name="from_user", db_index=True)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Recipient",
                                  related_name="to_user", db_index=True)
    text = models.TextField(verbose_name="Text", blank=True)
    file = models.ForeignKey(UploadedFile, related_name='message',  on_delete=models.DO_NOTHING,
                             verbose_name="file", blank=True, null=True)
    read = models.BooleanField(verbose_name=_('File'), default=False)
    all_objects = models.Manager()

    @staticmethod
    def get_unread_count_for_dialog_with_user(sender, recipient):
        return MessageModel.objects.filter(sender_id=sender, recipient_id=recipient, read=False).count()

    @staticmethod
    def get_last_message_for_dialog(sender, recipient):
        return MessageModel.objects.filter(
            Q(sender_id=sender, recipient_id=recipient) | Q(sender_id=recipient, recipient_id=sender)) \
            .select_related('sender', 'recipient').first()

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super(MessageModel, self).save(*args, **kwargs)
        DialogsModel.create_if_not_exists(self.sender, self.recipient)

    class Meta:
        ordering = ('-created',)
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")