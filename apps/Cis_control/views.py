from .models import CisControl

from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render


def controls_list(request):
    controls = CisControl.objects.all().order_by('id')  # یا هر ترتیبی که بخواهی
    return render(request, 'ControlList.html', {'controls': controls})
