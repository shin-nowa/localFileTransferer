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
    
    #salvando data e hora quando o log for criado
    timestamp = models.DateTimeField(auto_now_add=True)
    
    ip_address = models.GenericIPAddressField(null = True, blank = True)
    
    def __str__(self):
        # o que aparece na lista do adm
        return f"{self.user.username} - {self.action} - {self.file_name}"
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    
    active_directory = models.CharField(max_length=2048, null = True, blank = True)
    
    def __str__(self):
        return f"Perfil de {self.user.username}"
@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
@receiver(post_save, sender = User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
# Create your models here.
