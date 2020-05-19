from django.db import models
from django.utils import timezone # needed for timestamp of publish, created, & updated attributes
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length = 250)
    slug = models.SlugField(max_length = 250, unique_for_date = 'publish')
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default = timezone.now) # date with timezone info
    created = models.DateField(auto_now_add = True) # date when post initially created
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length = 10, choices = STATUS_CHOICES, default = 'draft')

    class Meta:     # just a class container with some options (metadata)
        ordering = ('-publish', )   # the negative puts in descending order from most recently pubished

    def __str__(self):   # creates a human-readable representation of the object
        return self.title


