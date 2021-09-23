from django.db import models
from projectFocusapi.models.lot_note import LotNote
from projectFocusapi.models.project import Project


class Lot(models.Model):

    lotSize = models.CharField(max_length=150)
    lotNumber = models.IntegerField()
    super = models.ForeignKey("Super", on_delete=models.CASCADE)


    @property
    def lot_lot_notes(self):
        lotlotnotes = LotNote.objects.filter(lotId=self)
        return lotlotnotes 
    @property
    def lot_projects(self):
        projects = Project.objects.filter(lotId=self)
        return projects 