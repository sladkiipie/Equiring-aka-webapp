from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

from users.models import User



def user_status_change(sender, instance, **kwargs):
    GROUP_BY_STATUS = {
        'approved': 'user_without_contract',
        'rejected': 'deleted_user',
    }

    if instance.status in GROUP_BY_STATUS:
        status = GROUP_BY_STATUS[instance.status]
        instance.groups.clear()
        group = Group.objects.get(name=status)
        group.user_set.add(instance)


@receiver(post_save, sender=User)
def track_user_status_change(sender, instance, created, update_fields=None, **kwargs):
    if created:
        return

    if update_fields and 'status' not in update_fields:
        return

    user_status_change(instance, instance.status)



