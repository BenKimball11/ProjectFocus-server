from django.db import models


class Lot(models.Model):
    """Game Model
    Fields:
        models (CharField): The name of the game
        game_type (ForeignKey): The type of game
        description (CharField): The description of the game
        number_of_players (IntegerField): The max number of players of the game
        maker (CharField): The company that made the game
    """
    name = models.CharField(max_length=100)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    lotSize = models.CharField(max_length=150)
    lotNumber = models.IntegerField()
    super = models.ForeignKey("Super", on_delete=models.CASCADE)