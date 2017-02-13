from django.db import models

# Create your models here.

class Request_HTML(models.Model):
  """docstring for ClassName"""
  url_html = models.TextField()
  source_html = models.TextField()
  #header_http = models.TextField()
  class Meta:
    db_tablespace = "tables"

class RequestAgatBusy(models.Model):
  url_html = models.CharField(max_length=200)
  header_http = models.TextField()
  source_html = models.TextField()






