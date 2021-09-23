from django.db import models
from projectFocusapi.models.project_note import ProjectNote


class Project(models.Model):
    """Game Model
    Fields:
        models (CharField): The name of the game
        game_type (ForeignKey): The type of game
        description (CharField): The description of the game
        number_of_players (IntegerField): The max number of players of the game
        maker (CharField): The company that made the game
    """
    name = models.CharField(max_length=100)
    lotId = models.ForeignKey("lot", on_delete=models.CASCADE)
    estimatedCompletionDate = models.DateField()
    estimatedCost = models.IntegerField()
    #notes = models.ManyToManyField("Note", through="ProjectNote")

    @property
    def project_notes(self):
        projectnotes = ProjectNote.objects.filter(projectId=self)
        return projectnotes 
    