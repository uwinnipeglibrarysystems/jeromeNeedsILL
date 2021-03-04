from uuid import uuid4

from django.db import models

# Create your models here.

class illrequestbase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    date_created = models.DateTimeField(
        auto_now_add=True, blank=False)
    
class openurlrequest(models.Model):
    request = models.ForeignKey(illrequestbase, on_delete=models.CASCADE,
                                blank=True, db_index=False)
    key = models.CharField(max_length=255, blank=False)
    value = models.CharField(max_length=255, blank=False)

    class Meta:
        indexes=[
            models.Index(fields=['request', 'key'])]
            
