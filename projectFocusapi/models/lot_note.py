from django.db import models

class LotNote(models.Model):
    """Join model for Events and Gamers
    """
    lot = models.ForeignKey("Lot", on_delete=models.CASCADE)
    note = models.ForeignKey("Note", on_delete=models.CASCADE)