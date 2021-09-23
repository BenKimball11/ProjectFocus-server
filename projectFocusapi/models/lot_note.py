from django.db import models


class LotNote(models.Model):
    
    name = models.TextField()
    lotId = models.ForeignKey("Lot", on_delete=models.CASCADE)
    date = models.DateField()
    itemsReceived = models.TextField()
    description = models.CharField(max_length=100)
    contactNumber = models.IntegerField()