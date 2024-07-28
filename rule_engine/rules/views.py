from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Rule, UserAttribute
from .serializers import RuleSerializer, UserAttributeSerializer
from .ast import create_rule, combine_rules, evaluate_rule

class RuleViewSet(viewsets.ModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer

    @action(detail=False, methods=['post'])
    def combine(self, request):
        rules = request.data.get('rules', [])
        combined_ast = combine_rules(rules)
        return Response(combined_ast)

class UserAttributeViewSet(viewsets.ModelViewSet):
    queryset = UserAttribute.objects.all()
    serializer_class = UserAttributeSerializer

    @action(detail=False, methods=['post'])
    def evaluate_rule(self, request):
        rule_id = request.data.get('rule_id')
        user_data = request.data.get('user_data')
        rule = Rule.objects.get(id=rule_id)
        result = evaluate_rule(rule.ast_json, user_data)
        return Response({'result': result})
