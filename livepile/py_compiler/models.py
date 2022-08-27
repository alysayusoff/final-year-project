from django.db import models

# Create your models here.
class Room(models.Model):
    room_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.room_name}"

    def get_number_of_participants(self):
        return self.participants.all().count()

    def get_participants(self):
        return self.participants.all()

class Participant(models.Model):
    username = models.CharField(max_length=255)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='participants')

    def __str__(self):
        return f"{self.username}"