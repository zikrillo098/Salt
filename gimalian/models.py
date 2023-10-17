from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Category(models.Model):
    title = models.CharField(max_length=155)

    def __str__(self):
        return self.title


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=155)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    tags = TaggableManager()
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PUBLISHED)
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']

    def __str__(self): return self.title

    def get_absolute_url(self):
        return reverse('gimalian:post_detail', args=[
            self.publish.year,
            self.publish.month,
            self.publish.day,
            self.slug])
