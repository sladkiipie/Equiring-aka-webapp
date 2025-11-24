from django.contrib import admin

from supports.models import SupporTicket, SupportMessage

supports_models = [
    admin.site.register(SupporTicket),
    admin.site.register(SupportMessage)
]