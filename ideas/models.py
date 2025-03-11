from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    main_image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    content = RichTextUploadingField()  # CKEditor Rich Text Editor
    tags = models.ManyToManyField('Tag')
    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title