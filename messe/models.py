from django.db import models


class Message(models.Model):
  username = models.CharField(max_length=100)
  body = models.TextField()
  ip_address = models.CharField(
      max_length=50, blank=True, null=True
  )  # IP uchun
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.username}: {self.body[:20]}"