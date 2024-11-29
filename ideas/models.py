from django.db import models
from django.contrib.auth.models import User  # For user accounts

class Idea(models.Model):
    title = models.CharField(max_length=200)  # Short title of the idea
    content = models.TextField()  # Detailed content of the idea
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # User who submitted it
    timestamp = models.DateTimeField(auto_now_add=True)  # Time of submission

    def __str__(self):
        return self.title  # What shows up in the admin panel
    
class Comment(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
