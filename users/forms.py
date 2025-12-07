from django.forms import ModelForm
from django.contrib.auth.forms import SetPasswordForm

from supports.models import SupporTicket
from .models import User

class PrimaryUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name','email', 'phone_number', 'message']

class TicketForm(ModelForm):
    class Meta:
        model = SupporTicket()
        fields = ['contract', 'description']
