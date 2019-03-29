from django.db import models

# Create your models here.
class Search(models.Model):
    query = models.CharField(max_length=500, null=False, blank=False)




