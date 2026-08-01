from django.db import models


class Message(models.Model):
  username = models.CharField(max_length=100)
  body = models.TextField(blank=True, null=True)  # Matn bo'sh bo'lishi mumkin (faqat rasm yuborganda)
  image = models.ImageField(
      upload_to='chat_images/', blank=True, null=True
  )  # Rasm uchun
  ip_address = models.CharField(max_length=50, blank=True, null=True)
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.username}: {self.body[:20] if self.body else '[Rasm]'}"