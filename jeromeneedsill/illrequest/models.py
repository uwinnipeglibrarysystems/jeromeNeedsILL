# Copyright (c) 2021 University of Winnipeg
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from uuid import uuid4

from django.db import models

# Create your models here.

# length 60 to cover the extreme case in ipv6, of an IPv4 mapped IPv6
# address with a 15 character scope or zone after it (Linux max)
# https://stackoverflow.com/questions/166132/maximum-length-of-the-textual-representation-of-an-ipv6-address
IP_ADDR_LENGTH = 60

class illrequestbase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    date_created = models.DateTimeField(
        auto_now_add=True, blank=False)

class illrequestdiscoveredipaddress(models.Model):
    request = models.ForeignKey(illrequestbase, on_delete=models.CASCADE,
                                blank=False, db_index=True)
    original_ip = models.CharField(max_length=IP_ADDR_LENGTH, blank=False)
    outside_ip = models.CharField(max_length=IP_ADDR_LENGTH, blank=False)
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
    ip = models.CharField(max_length=IP_ADDR_LENGTH, blank=False)
