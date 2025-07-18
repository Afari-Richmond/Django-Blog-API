from django.db import models
import uuid

from django.contrib.auth.models import User


class BaseModel(models.Model):
    uid = models.UUIDField(
    primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class Blog(BaseModel):  # create a Blog Model which inherits from the base model
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=500)
    blogtext = models.TextField()
    main_image = models.ImageField(upload_to='blogs')

    def __str__(self):
        return self.title
