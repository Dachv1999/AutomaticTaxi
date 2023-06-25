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
from .models import Enterprise
from ManageVehicles.models import Invoice
from .serializers import InvoiceSerializer, AllInvoiceSerializer, InvoiceSerializer
from django.db.models import Q
from django.http import HttpResponse, JsonResponse

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
 
 
 pdf = PDF("Repair Invoice")
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


@api_view(['GET'])
def create_report_invoice(request, start_date, end_date):
  
   if start_date != "0" and end_date != "0":
     
     start_date_ = datetime.strptime(start_date, '%Y-%m-%d').date()
     end_date_ = datetime.strptime(end_date, '%Y-%m-%d').date()


     invoices = Invoice.objects.filter(
        Q(created_at__gte=start_date_) & Q(created_at__lte=end_date_))
      
     serializedData = InvoiceSerializer(invoices, many = True)

   else:

      invoices = Invoice.objects.all()
      serializedData = InvoiceSerializer(invoices, many =True)

     
   pdf = PDF("Invoice Report")
   pdf.add_page()
   pdf.date_body("Start Date: "+ str(start_date_),0)
   pdf.date_body("End Date: "+ str(end_date_),1)

   total = 0

   for i in invoices:
      pdf.chapter_body("NIT: " + i.nit)
      pdf.chapter_body("Plate: " + i.plate)
      pdf.chapter_body("Company Name: " + i.id_empresa.enterprise_name)
      pdf.chapter_body("Creation Date: " + str(i.created_at))
      pdf.chapter_body_line("Service Description: " + i.service_desc)
      pdf.chapter_price("Total Invoice: " + str(i.price))
      total += i.price


   pdf.chapter_body_line("Total Price: " + str(total))
   titlepdf = str(uuid.uuid4()) + ".pdf"
   pdf.output(titlepdf, 'F')


   import subprocess


   #pdf_file_path = "titulo_pdf.pdf"
   command = f'start "" "{titlepdf}"'
   subprocess.run(command, shell=True)
   

   
   return Response({'status_code':status.HTTP_200_OK,
                    'transactions':serializedData.data})




