from django.contrib import admin

from users.models import *

users_models = [
    admin.site.register(User),
    admin.site.register(Companies),
    admin.site.register(Contracts),
    admin.site.register(Transactions),
    admin.site.register(Application),
    admin.site.register(ApplicationCheck)
]
