from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.core.mail import send_mail

from .models import User, RegistrationToken



def user_status_change(sender, instance, **kwargs): # функция изменения группы пользователей в зависимости от изменения статуса
    GROUP_BY_STATUS = {
        'approved': 'user_without_contract',
        'rejected': 'deleted_user',
    }

    if instance.status in GROUP_BY_STATUS: # проверка есть ли статус в словаре, и присвоение группы
        status = GROUP_BY_STATUS[instance.status]
        instance.groups.clear()
        group = Group.objects.get(id=id)
        group.user_set.add(status)

        if status == 'approved': # отправка mail письма на создание аккаунта
            token = RegistrationToken.objects.create(user=instance)
            link = f"{settings.SITE_URL}/set-password/{token.token}/"

            send_mail(
                subject="регистрация на сайте",
                message=f"Прив ет {instance.name}, установите пароль по ссылке {link}",
                from_email = settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
            )



@receiver(post_save, sender=User) # триггер на изменение статуса пользователя
def track_user_status_change(sender, instance, created, update_fields=None, **kwargs):
    if created:
        return

    if update_fields and 'status' not in update_fields:
        return

    user_status_change(instance, instance.status)



