from django.db import models


class ProjectNote(models.Model): 
    name = models.TextField()
    projectId = models.ForeignKey("project", on_delete=models.CASCADE)
    date = models.DateField()
    itemsReceived = models.TextField()
    description = models.CharField(max_length=100)
    contactNumber = models.IntegerField()