from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """
    Sempre que um User é criado (ou salvo), garantimos que exista um Profile associado.
    Isso permite chamar `request.user.profile` em templates/views sem erros.
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        # garante que existe caso uma migração antiga não tenha criado
        Profile.objects.get_or_create(user=instance)
