from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Invoice
from .serializers import InvoiceSerializer, AllInvoiceSerializer

@api_view(['GET'])
def getPayInvoice(request):
    
    invoices = Invoice.objects.filter(is_pay=True).order_by('updated_at')
    serializedData = InvoiceSerializer(invoices, many=True)

    return Response({
        'status_code': status.HTTP_200_OK,
        'transactions': serializedData.data
    })
