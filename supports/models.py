import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel, SoftDeletableModel
from django.db.models import Q
from typing import Optional, Any
from users.models import User, Contracts


def user_directory_path(instance, filename):
    return f"user_{instance.uploaded_by.pk}/{filename}"

class UploadedFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Uploaded_by",
                                    related_name="+", db_index=True)
    file = models.FileField(verbose_name="File", blank=False, null=False, upload_to=user_directory_path)
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="Uploaded date")

    def __str__(self):
        return self.file.name

class SupporTicket(TimeStampedModel):
    STATUS_CHOICES = [     # Выбор статуса. По примеру сделать контракт со следующими переменными: НА РАССМОТРЕНИИ, ПРИНЯТ, ОТКАЗАНО!
        ('opened', 'Открыт'),
        ('closed', 'Закрыт'),
        ('closedbyuser', 'Клиент отозвал'),
    ]
    id = models.BigAutoField(primary_key=True, verbose_name="id")
    asker_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="User1",
                              related_name="+", db_index=True)
    responsible_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="User2",
                              related_name="+", db_index=True)
    contract = models.ForeignKey(Contracts, related_name="contract", on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='opened')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user1', 'user2'], name="unique_dialogs"),
            models.UniqueConstraint(fields=['user2', 'user1'], name="unique_dialogs_reversed")
        ]
        verbose_name = "Dialogs"
        verbose_name_plural = "Dialogs"

    def __str__(self):
        return _("Dialogs beetwen ") + f"{self.asker_id} {self.responsible_id}"

    @staticmethod
    def dialog_exists(u1: User, u2: User) -> Optional[Any]:
        return SupporTicket.objects.filter(Q(user1=u1, user2=u2) | Q(user2=u2, user1=u1)).first()

    @staticmethod
    def create_if_not_exists(u1: User, u2: User): # Попробовать указать модель User если не будет рабоать
        res = SupporTicket.dialog_exists(u1, u2)
        if not res:
            SupporTicket.objects.create(user1=u1, user2=u2)

    @staticmethod
    def get_dialogs_for_user(user: User): # Попробовать указать модель User если не будет рабоать
        return SupporTicket.objects.filter(Q(user1=user) | Q(user2=user)).values_list('user1_id', 'user2_id')

class TicketMessage(TimeStampedModel, SoftDeletableModel):
    id = models.BigAutoField(primary_key=True, verbose_name="id")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Author",
                               related_name="from_user", db_index=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Responsible",
                                  related_name="to_user", db_index=True)
    text = models.TextField(verbose_name="Text", blank=True)
    file = models.ForeignKey(UploadedFile, related_name='message',  on_delete=models.DO_NOTHING,
                             verbose_name="file", blank=True, null=True)
    read = models.BooleanField(verbose_name=_('File'), default=False)
    all_objects = models.Manager()

    @staticmethod
    def get_unread_count_for_dialog_with_user(sender, recipient):
        return TicketMessage.objects.filter(sender_id=sender, recipient_id=recipient, read=False).count()

    @staticmethod
    def get_last_message_for_dialog(sender, recipient):
        return TicketMessage.objects.filter(
            Q(sender_id=sender, recipient_id=recipient) | Q(sender_id=recipient, recipient=sender)) \
            .select_related('sender_id', 'recipient_id').first()

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        super(TicketMessage, self).save(*args, **kwargs)
        SupporTicket.create_if_not_exists(self.sender, self.recipient)

    class Meta:
        ordering = ('-created',)
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")