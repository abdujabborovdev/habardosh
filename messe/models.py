from django.db import models


class Message(models.Model):
  username = models.CharField(max_length=100)  # Foydalanuvchi kiritgan ism
  body = models.TextField()  # Xabar matni
  created = models.DateTimeField(auto_now_add=True)  # Vaqti

  def __str__(self):
    return f"{self.username}: {self.body[:20]}"