from django.db import models

# Create your models here.
class illrequest(models.Model):
    # these fields are modeled on Relais ILL Add_Request
    # https://help.oclc.org/Resource_Sharing/Relais_ILL/Relais_Web_services/Add_Request
    # though not all have been included
    
    biblio_title = models.CharField(max_length=255, blank=True)
    bilio_author = models.CharField(max_length=255, blank=True)
    bilio_subtitle = models.CharField(max_length=255, blank=True)
    bilio_seriestitle = models.CharField(max_length=255, blank=True)
    bilio_edition = models.CharField(max_length=255, blank=True)
    bilio_articletitle = models.CharField(max_length=255, blank=True)
    bilio_articleauthor = models.CharField(max_length=255, blank=True)
    bilio_volume = models.CharField(max_length=255, blank=True)
    bilio_issue = models.CharField(max_length=255, blank=True)
    bilio_physdescription = models.CharField(max_length=255, blank=True)
    bilio_itemorfoldernumber = models.CharField(max_length=255, blank=True)
    bilio_accessionnum = models.CharField(max_length=255, blank=True)
    bilio_boxnum = models.CharField(max_length=255, blank=True)
    bilio_imageorpagenum = models.IntegerField(blank=True)
    bilio_pagesrequested = models.CharField(max_length=255, blank=True)
    bilio_estimatedpages = models.CharField(max_length=255, blank=True)
    bilio_issn1 = models.CharField(max_length=255, blank=True)
    bilio_issn2 = models.CharField(max_length=255, blank=True)
    bilio_isbn1 = models.CharField(max_length=255, blank=True)
    bilio_isbn2 = models.CharField(max_length=255, blank=True)
    bilio_ismn = models.CharField(max_length=255, blank=True)
    bilio_callnumber = models.CharField(max_length=255, blank=True)
    bilio_additionalnumbers = models.CharField(max_length=255, blank=True)
    bilio_sponsor = models.CharField(max_length=255, blank=True)
    bilio_informationsource = models.CharField(max_length=255, blank=True)
    bilio_oclcrecno = models.CharField(max_length=255, blank=True)
    bilio_system = models.CharField(max_length=255, blank=True)
    bilio_systemnum = models.CharField(max_length=255, blank=True)
    bilio_lccn = models.CharField(max_length=255, blank=True)
    bilio_bibliography = models.CharField(max_length=255, blank=True)
    bilio_bibliographynumber = models.CharField(max_length=255, blank=True)
    bilio_bibid = models.CharField(max_length=255, blank=True)
    bilio_localitemfound = models.CharField(max_length=255, blank=True)

    location_supplycode = models.CharField(max_length=255, blank=True)
    location_supplybibid = models.CharField(max_length=255, blank=True)
    location_supplyitemid = models.CharField(max_length=255, blank=True)
    location_supplycallnum = models.CharField(max_length=255, blank=True)
    location_supplysummaryholdings = models.CharField(
        max_length=255, blank=True)
    location_description = models.CharField(max_length=255, blank=True)
    location_bibid = models.CharField(max_length=255, blank=True)
    location_itemid = models.CharField(max_length=255, blank=True)
    location_callnum = models.CharField(max_length=255, blank=True)
    location_summaryholdings = models.CharField(max_length=255, blank=True)

    publisher_name = models.CharField(max_length=255, blank=True)
    publisher_publicationtype = models.CharField(max_length=255, blank=True)
    publisher_publicationdate = models.DateField(blank=True)
    publisher_publicationplace = models.CharField(max_length=255, blank=True)

    requestinfo_servicetype = models.CharField(max_length=255, blank=True)
    requestinfo_servicetype = models.CharField(max_length=255, blank=True)
    requestinfo_servicelevel = models.CharField(max_length=255, blank=True)
    requestinfo_requestsource = models.CharField(max_length=255, blank=True)
    requestinfo_datesubmitted = models.DateTimeField(
        auto_now_add=True, blank=False)
    requestinfo_notes = models.CharField(max_length=255, blank=True)
    requestinfo_mailbox = models.CharField(max_length=255, blank=True)
    requestinfo_nlmuniqueid = models.CharField(max_length=255, blank=True)
    requestinfo_externalnumber = models.CharField(max_length=255, blank=True)
    requestinfo_expirydate = models.DateField(blank=True)
    requestinfo_needbydate = models.DateField(blank=True)
    requestinfo_maxcost = models.CharField(max_length=255, blank=True)
    requestinfo_projectcode = models.CharField(max_length=255, blank=True)
    requestinfo_agreedtermsconditions = models.BooleanField(null=True)
    requestinfo_copyrightcomply = models.BooleanField(null=True)

    # requestinfo_requester left out as that will be a
    # reference to another model once developed
    
    electronic_documentpath = models.CharField(max_length=255, blank=True)
    electronic_supplycode = models.CharField(max_length=255, blank=True)

    sysnum_oclcnum = models.CharField(max_length=255, blank=True)
    sysnum_opacnumb = models.CharField(max_length=255, blank=True)
    sysnum_medlinenum = models.CharField(max_length=255, blank=True)
    sysnum_doclinenum = models.CharField(max_length=255, blank=True)
    sysnum_doclineflag = models.CharField(max_length=255, blank=True)

    electronicdelivery_fileformat = models.CharField(max_length=255, blank=True)
    electronicdelivery_outputformat = models.CharField(
        max_length=255, blank=True)
    electronicdelivery_deliverymethod = models.CharField(
        max_length=255, blank=True)
    electronicdelivery_deliveryaddress = models.CharField(
        max_length=255, blank=True)
    electronicdelivery_messagingmethod = models.CharField(
        max_length=255, blank=True)
    electronicdelivery_messagingaddress = models.CharField(
        max_length=255, blank=True)

class openurlrequest(models.Model):
    request = models.ForeignKey(illrequest, on_delete=models.CASCADE,
                                blank=False, db_index=False)
    key = models.CharField(max_length=255, blank=False)
    value = models.CharField(max_length=255, blank=False)

    class Meta:
        indexes=[
            models.Index(fields=['request', 'key'])]
            
