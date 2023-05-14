from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Customer

#class CreateCustomerView(APIView):
#    parser_classes = FormParser
#    def post(self, request, format=None):
#        data = self.request.data

#        ac