from django.db import models

class Rule(models.Model):
    rule_string = models.TextField()
    ast_json = models.JSONField()

class UserAttribute(models.Model):
    user_id = models.IntegerField(unique=True)
    age = models.IntegerField()
    department = models.CharField(max_length=100)
    salary = models.IntegerField()
    experience = models.IntegerField()
