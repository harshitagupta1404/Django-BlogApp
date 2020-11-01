from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)       #opens the image
        if img.height > 400 or img.width >300:
            output_size = (300,300)         # tuple of max size
            img.thumbnail(output_size)
            img.save(self.image.path)       # it will save this resized image at the same path (override it)