from django.db import models
import uuid, imghdr

# Create your models here.

class Picture(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    image = models.ImageField(upload_to='pictures/')
    title = models.CharField(max_length=100, blank=True)
    format = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.uuid}" #or f"Picture {self.uuid}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            self.image.open() 
            image_format = imghdr.what(self.image.file) 

            if image_format:
                self.format = image_format

            Picture.objects.filter(uuid=self.uuid).update(format=self.format)


class UserInfo(models.Model):
    user_agent = models.CharField(max_length=256)
    ip = models.CharField(max_length=256)
    picture = models.ForeignKey(Picture, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    message_id = models.CharField(max_length=256, null=True)
    user_id = models.CharField(max_length=256, null=True)

    def __str__(self) -> str:
        return self.user_agent