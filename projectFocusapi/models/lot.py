from django.db import models
from projectFocusapi.models.lot_note import LotNote
from projectFocusapi.models.project import Project


class Lot(models.Model):
    """Game Model
    Fields:
        models (CharField): The name of the game
        game_type (ForeignKey): The type of game
        description (CharField): The description of the game
        number_of_players (IntegerField): The max number of players of the game
        maker (CharField): The company that made the game
    """
    lotSize = models.CharField(max_length=150)
    lotNumber = models.IntegerField()
    super = models.ForeignKey("Super", on_delete=models.CASCADE)
    notes = models.ManyToManyField("Note", through="LotNote")


    @property
    def lot_notes(self):
        notes = LotNote.objects.filter(lot=self)
        return notes 
    @property
    def lot_projects(self):
        projects = Project.objects.filter(lotId=self)
        return projects 