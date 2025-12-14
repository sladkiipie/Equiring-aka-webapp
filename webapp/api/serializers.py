from rest_framework.serializers import ModelSerializer
from supports.models import SupporTicket
from users.models import  Contracts

class TicketSerializer(ModelSerializer):
    class Meta:
        model = SupporTicket
        fields = '__all__'  


class ContractsSerializer(ModelSerializer):
    class Meta:
        model = Contracts
        fields = '__all__'