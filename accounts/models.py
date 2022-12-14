from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class User(AbstractUser):
    followings = models.ManyToManyField("self", symmetrical=False, related_name="followers")
    profile = ProcessedImageField(upload_to='image/', blank=True,
                                processors=[ResizeToFill(50, 50)],
                                format='JPEG',
                                options={'quality': 80})