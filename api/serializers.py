from rest_framework import serializers
from .models import BankParam


class BankAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankParam
        fields = "__all__"
