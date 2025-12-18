import uuid

from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models import OneToOneField
from django.contrib.contenttypes.models import ContentType

from supports import permisions

# Создание менеджера пользователей
class MyUserManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError("User must have a login")
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self.create_user(login, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('reject', 'Reject'),
        ('pending', 'Pending'),
    ]

    login = models.CharField(max_length=255, unique=True, verbose_name='login')
    password = models.CharField(max_length=128) # паоль хешиоруется на стороке бекенда
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')


    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'login'

    def __str__(self):
        return self.login
    class Meta:
     permissions = [('', )]

def token_expired_at():
    return timezone.now() + timezone.timedelta(hours=24)

class RegistrationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=token_expired_at)
    used = models.BooleanField(default=False)

    def is_valid(self):
        return not self.used and timezone.now() < self.expires_at

class Companies(models.Model):
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('reject', 'Reject'),
        ('pending', 'Pending'),
        ('freeze', 'Freeze'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    INN = models.BigIntegerField()
    OGRN = models.BigIntegerField()
    name_company = models.CharField(max_length=255)
    founder = models.ManyToManyField(User, related_name='founder')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.name_company

class Contracts(models.Model):
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('reject', 'Reject'),
        ('pending', 'Pending'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Companies, related_name='company', on_delete=models.CASCADE)
    name_contract = models.CharField(max_length=255)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='pending') # документ должен быть в темплейтс или еще где будем просто вызывать док пользовательского соглашения  он одинаков для всех

    def __str__(self):
        return self.name_contract


class Transactions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contract = models.ForeignKey(Contracts, on_delete=models.CASCADE)
    ammount = models.DecimalField(max_digits=10, decimal_places=2)
    type_transaction = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    sender_agreement = models.UUIDField(null=True)
    recipient_agreement = models.UUIDField(null=True)
    data_trasaction = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type_transaction

class Application(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='application_owner')
    type_request = models.CharField(max_length=255)
    message = models.TextField()
    for_company = models.ManyToManyField(Companies, related_name='application_for_company')
    for_contract = models.ManyToManyField(Contracts, related_name='application_for_contract')
    application_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.type_request

class ApplicationCheck(models.Model):
    application_id = models.IntegerField(OneToOneField(Application, on_delete=models.CASCADE))
    approved = models.IntegerField()
    action = models.CharField(max_length=255)
    application_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.application_id

# Классы подмоделей в виде прокси

class Client(User):
    class Meta:
        proxy = True
        permissions = [('can_login')]
        
        
        
class ClientFull(User):
    class Meta:
        proxy = True
        permissions = [('can_create_contract', 'can_create_ticket','can_close_ticket','can_create_company','can_update_company')]
        content_type = ContentType.objects.get_for_model(ClientFull, for_concrete_model=False)
        clientfull_permissions = permissions.objects.filter(content_type=content_type)
        [p.codename for p in clientfull_permissions]
        ['can_create_contract', 'can_create_ticket','can_close_ticket','can_create_company','can_update_company']
        for permission in clientfull_permissions:
                User.user_permissions.add(permission)
        User.has_perms((''))
        True



class SupManager(User):
    class Meta:
        proxy = True
        permissions = [('can_update_contract', 'can_update_supticket','can_update_application',)]
        content_type = ContentType.objects.get_for_model(SupManager, for_concrete_model=False)
        supmanager_permissions = permissions.objects.filter(content_type=content_type)
        [p.codename for p in supmanager_permissions]
        ['app.can_update_application','app.can_update_contract', 'app.can_update_ticket']
        for permission in supmanager_permissions:
                User.user_permissions.add(permission)
        User.has_perms(('app.can_update_application','app.can_update_contract', 'app.can_update_ticket'))
        True
        
        
        
        
        

    
        
