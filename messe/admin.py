from django.contrib import admin
from .models import Message

# Message modelini admin panelga qo'shish
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('username', 'body', 'ip_address', 'created') # Admin panelda ko'rinadigan ustunlar
    search_fields = ('username', 'body', 'ip_address')            # Qidirish uchun maydonlar