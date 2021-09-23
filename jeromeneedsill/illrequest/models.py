from uuid import uuid4

from django.db import models

# Create your models here.

class illrequestbase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    date_created = models.DateTimeField(
        auto_now_add=True, blank=False)

class illmanualrequester(models.Model):
    request = models.ForeignKey(illrequestbase, on_delete=models.CASCADE,
                                blank=False, db_index=True)
    requester_name = models.CharField(max_length=255, blank=False)
    email = models.CharField(max_length=255, blank=False)
    barcode = models.CharField(max_length=255, blank=False)
    
class openurlrequest(models.Model):
    request = models.ForeignKey(illrequestbase, on_delete=models.CASCADE,
                                blank=True, db_index=False)
    key = models.CharField(max_length=255, blank=False)
    value = models.CharField(max_length=255, blank=False)

    class Meta:
        indexes=[
            models.Index(fields=['request', 'key'])]
            
class relaisrequestsmade(models.Model):
    request = models.ForeignKey(illrequestbase, on_delete=models.CASCADE,
                                blank=False, db_index=True)
    date_created = models.DateTimeField(
        auto_now_add=True, blank=False)
    barcode = models.CharField(max_length=255, blank=False)
    # length 60 to cover the extreme case in ipv6, of an IPv4 mapped IPv6
    # address with a 15 character scope or zone after it (Linux max)
    # https://stackoverflow.com/questions/166132/maximum-length-of-the-textual-representation-of-an-ipv6-address
    ip = models.CharField(max_length=60, blank=False)
