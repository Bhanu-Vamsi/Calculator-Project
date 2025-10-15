from django.db import models

# Create your models here.

class Calculation(models.Model):
    expression = models.CharField(max_length=255)
    operation = models.CharField(max_length=50)
    result = models.CharField(max_length=255, null=True, blank=True)
    error = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.expression} ({self.operation}) = {self.result or self.error}"
