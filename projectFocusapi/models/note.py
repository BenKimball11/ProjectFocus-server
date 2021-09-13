from django.db import models


class Note(models.Model):
    """Event Model
    Fields:
        host (ForeignKey): the user that made the event
        game (ForeignKey): the game associated with the event
        date (DateField): The date of the event
        time (TimeFIeld): The time of the event
        description (TextField): The text description of the event
        title (CharField): The title of the event
        attendees (ManyToManyField): The gamers attending the event
    """
    super = models.ForeignKey("Super", on_delete=models.CASCADE)
    name = models.TextField()
    lot = models.ForeignKey("Lot", on_delete=models.CASCADE)
    date = models.DateField()
    itemsReceived = models.TextField()
    note = models.CharField(max_length=100)
    contactNumber = models.IntegerField()