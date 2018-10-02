from django.db import models
from django.contrib.auth.models import AbstractUser

class Chatroom(models.Model):
	no_of_users=models.PositiveSmallIntegerField(default=0)
	name=models.CharField(max_length=20)
class User(AbstractUser):
	current_chat_room=models.ForeignKey(Chatroom,null=True,blank=True,on_delete=models.CASCADE)
