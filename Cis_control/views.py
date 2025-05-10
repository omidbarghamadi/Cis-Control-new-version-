from .models import CisControl
from .serializers import CisControlSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render


def landing_page(request):
    return render(request, 'index.html')


def controls_list(request):
    controls = CisControl.objects.all().order_by('id')  # یا هر ترتیبی که بخواهی
    return render(request, 'ControlList.html', {'controls': controls})


class CisControlListView(APIView):
    permission_classes = []

    def get(self, request):
        controls = CisControl.objects.all()

        serializer = CisControlSerializer(controls, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
