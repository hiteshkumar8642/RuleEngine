from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Rule
from .serializers import RuleSerializer
from .ast import create_rule, combine_rules, evaluate_ast

class RuleViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def create_rule(self, request):
        rule_string = request.data.get('rule_string')
        if not rule_string:
            return Response({'error': 'Rule string is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        ast_json = create_rule(rule_string)
        rule = Rule.objects.create(rule_string=rule_string, ast_json=ast_json)
        return Response({'id': rule.id,'rule_string': rule_string, 'ast_json': ast_json}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def combine(self, request):
        rules = request.data.get('rules', [])
        ast_json = request.data.get('ast_json', None)
        if not rules:
            return Response({'error': 'At least one rule is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        combined_ast = combine_rules(rules, ast_json)
        return Response(combined_ast)

class UserAttributeViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def evaluate_rule(self, request):
        rule_id = request.data.get('rule_id')
        user_data = request.data.get('user_data')
        if not rule_id or not user_data:
            return Response({'error': 'Rule ID and user data are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            rule = Rule.objects.get(id=rule_id)
        except Rule.DoesNotExist:
            return Response({'error': 'Rule not found'}, status=status.HTTP_404_NOT_FOUND)
        
        result = evaluate_ast(rule.ast_json, user_data)
        return Response({'result': result})
