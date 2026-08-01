from django.db import models


class Message(models.Model):
  username = models.CharField(max_length=100)
  body = models.TextField(blank=True, null=True)
  image = models.ImageField(upload_to='chat_images/', blank=True, null=True)
  ip_address = models.GenericIPAddressField(
      blank=True, null=True
  )  # IP manzil uchun
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.username}: {self.body}'