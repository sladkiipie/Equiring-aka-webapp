import uuid

from django.db import models
from django.db.models import ForeignKey

from users.models import Contracts, User


class SupporTicket(models.Model):
    STATUS_CHOICES = [     # Выбор статуса. По примеру сделать контракт со следующими переменными: НА РАССМОТРЕНИИ, ПРИНЯТ, ОТКАЗАНО!
        ('opened', 'Открыт'),
        ('closed', 'Закрыт'),
        ('closedbyuser', 'Клиент отозвал'),]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contract = models.ForeignKey(Contracts, related_name='contract', blank=True,on_delete=models.CASCADE)
    responsible_id = models.ForeignKey(User, related_name='supporter', blank=True,on_delete=models.CASCADE)
    asker_id = models.ForeignKey(User, related_name='asker', blank=True,on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='opened')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

class SupportMessage(models.Model):
    ticket_id = models.UUIDField(ForeignKey(SupporTicket, default=uuid.uuid4, editable=False, on_delete=models.CASCADE))
    message = models.CharField(max_length=255)
    date_message = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message