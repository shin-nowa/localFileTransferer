from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class TransferLog(models.Model):
    ACTIONS_CHOICES = [
        ('UPLOAD', 'Upload'),
        ('DONWLOAD', 'Download')
    ]

    #Conectando o log ao usuário que fez a ação
    # Se o usuário for deletado, o log ainda fica lá
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True, blank = True)
    
    action = models.CharField(max_length=10, choices=ACTIONS_CHOICES)
    file_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField(default = 0)
    
    #salvando data e hora quando o log for criado
    timestamp = models.DateTimeField(auto_now_add=True)
    
    ip_address = models.GenericIPAddressField(null = True, blank = True)
    
    def __str__(self):
        # o que aparece na lista do adm
        return f"{self.user.username} - {self.action} - {self.file_name}"
    
# Create your models here.
