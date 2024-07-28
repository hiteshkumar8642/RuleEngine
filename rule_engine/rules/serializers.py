from rest_framework import serializers
from .models import Rule, UserAttribute

class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'

class UserAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAttribute
        fields = '__all__'
