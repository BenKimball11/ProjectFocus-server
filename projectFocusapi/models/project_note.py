from django.db import models

class ProjectNote(models.Model):
    """Join model for Events and Gamers
    """
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    note = models.ForeignKey("Note", on_delete=models.CASCADE)