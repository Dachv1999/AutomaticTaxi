import json
from .Pdf import PDF
from django.utils import timezone
import uuid
from datetime import datetime
from pytz import timezone
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Invoice, Enterprise
from .serializers import InvoiceSerializer, AllInvoiceSerializer

@api_view(['GET'])
def getPayInvoice(request):
    
    invoices = Invoice.objects.filter(is_pay=True).order_by('-updated_at')
    serializedData = InvoiceSerializer(invoices, many=True)

    return Response({
        'status_code': status.HTTP_200_OK,
        'transactions': serializedData.data
    })

@api_view(['GET'])
def getNotPayInvoice(request):
    
    invoices = Invoice.objects.filter(is_pay=False).order_by('-updated_at')
    serializedData = InvoiceSerializer(invoices, many=True)

    return Response({
        'status_code': status.HTTP_200_OK,
        'transactions': serializedData.data
    })


@api_view(['GET'])    
def create_pdf(request, id_invoice):

 invoice = Invoice.objects.get(id=id_invoice)
 
 
 pdf = PDF()
 pdf.add_page()

 time_zone = timezone('America/New_York')
 date = datetime.now(time_zone)
 current_date = date.date()
 current_time = date.strftime('%H:%M')

 pdf.date_body("Expedite Date: "+ str(current_date),0)
 pdf.date_body("Expedite Time: "+ str(current_time),1)


 pdf.chapter_body("NIT: " + invoice.nit)
 pdf.chapter_body("Company Name: " + invoice.id_empresa.enterprise_name)
 pdf.chapter_body_line("Service Description: " + invoice.service_desc)
 pdf.chapter_body("Total Price: " + str(invoice.price))

 #titlepdf = str(id_invoice)+str(timezone.datetime.today()) + ".pdf"
 titlepdf = str(uuid.uuid4()) + ".pdf"
 pdf.output(titlepdf, 'F')


 import subprocess


 #pdf_file_path = "titulo_pdf.pdf"
 command = f'start "" "{titlepdf}"'
 subprocess.run(command, shell=True)
