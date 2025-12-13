from django.contrib import admin

from supports.models import SupporTicket, TicketMessage, UploadedFile

supports_models = [
    admin.site.register(SupporTicket),
    admin.site.register(TicketMessage),
    admin.site.register(UploadedFile),
]