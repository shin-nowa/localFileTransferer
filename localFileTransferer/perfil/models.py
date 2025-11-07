from django.db import models
from django.contrib.auth.models import User

def profile_picture_upload_to(instance, filename):
    """
    Path where profile pictures will be stored relative to MEDIA_ROOT.
    Example: uploads/profile_pictures/user_<id>/filename.jpg
    """
    return f"uploads/profile_pictures/user_{instance.user.id}/{filename}"

class Profile(models.Model):
    """
    Profile model linked 1-to-1 with Django's User.
    Stores the profile picture path (ImageField) and any other future metadata.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to=profile_picture_upload_to, null=True, blank=True)
    # você pode adicionar outros campos aqui no futuro sem quebrar a estrutura
    active_directory = models.CharField(max_length=2048, null=True, blank=True)
    def __str__(self):
        return f"Profile(user={self.user.username})"
