from django.db import models
from django.contrib.auth.models import AbstractUser

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'management/{0}/{1}'.format(instance.username, filename)

# Create your models here.
class User(AbstractUser):
    photo = models.ImageField(upload_to=user_directory_path)