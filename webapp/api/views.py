from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import Contracts
from supports.models import SupporTicket
from .serializers import ContractsSerializer, TicketSerializer
from webapp.api import serializers

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/suportticket',
        'GET /api/supportticket/:id'
    ]
    return Response(routes)


@api_view(['GET'])
def getContract(request):
    contracts = contracts.objects.all()
    serializer = ContractsSerializer(contracts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getContract(request):
    SupporTicket = SupporTicket.objects.all()
    serializer = TicketSerializer(SupporTicket, many=True)
    return Response(serializer.data)

