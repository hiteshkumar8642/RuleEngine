from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Rule

class RuleAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Sample rule data
        self.rule1 = {
            "rule_string": "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)",
        }

        self.rule2 = {
            "rule_string": "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)",
        }

    def test_create_rule(self):
        url = 'http://127.0.0.1:8000/rules/create_rule/'  
        response = self.client.post(url, self.rule1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.json())

    def test_combine_rules(self):
        url = 'http://127.0.0.1:8000/rules/combine/'  
        response = self.client.post(url, {
            'rules': [
                "age > 30",
                "department = 'Sales'"
            ],
            'ast_json': {
                "type": "operator",
                "value": "AND",
                "left": {
                    "type": "operand",
                    "value": "age > 30"
                },
                "right": {
                    "type": "operand",
                    "value": "department = 'Sales'"
                }
            }
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        combined_ast = response.json()
        self.assertIn('type', combined_ast)
        self.assertIn('value', combined_ast)

    def test_evaluate_rule(self):
        rule = Rule.objects.create(
            rule_string="(age > 30 AND department = 'Sales')",
            ast_json={
                "type": "operator",
                "value": "AND",
                "left": {
                    "type": "operand",
                    "value": "age > 30"
                },
                "right": {
                    "type": "operand",
                    "value": "department = 'Sales'"
                }
            }
        )
        url = 'http://127.0.0.1:8000/user_attributes/evaluate_rule/'  # Ensure this URL matches your `urls.py`
        response = self.client.post(url, {
            'rule_id': rule.id,
            'user_data': {
                'age': 35,
                'department': 'Sales',
                'salary': 60000,
                'experience': 4
            }
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['result'], True)

        response = self.client.post(url, {
            'rule_id': rule.id,
            'user_data': {
                'age': 25,
                'department': 'Marketing',
                'salary': 30000,
                'experience': 2
            }
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['result'], False)
