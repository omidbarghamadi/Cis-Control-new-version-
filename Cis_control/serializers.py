from rest_framework import serializers
from .models import CisControl


class CisControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = CisControl
        fields = ['id', 'title', 'description']
        read_only_fields = ['id']
