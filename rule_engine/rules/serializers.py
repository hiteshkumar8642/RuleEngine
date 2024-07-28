from rest_framework import serializers
from .models import Rule, UserAttribute

class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ['id', 'rule_string', 'ast_json']

class UserAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAttribute
        fields = ['user_id', 'age', 'department', 'salary', 'experience']
