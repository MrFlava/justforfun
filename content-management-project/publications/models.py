from datetime import datetime

from django.db import models

from processedmediafolders.models import ProcessedMediaFolder


class Topic(models.Model):
    name = models.CharField(max_length=255, default='')


class Publication(models.Model):
    created_at = models.DateTimeField(default=datetime.now())
    updated_at = models.DateTimeField(default=datetime.now())
    is_published = models.BooleanField(default=False)
    title = models.CharField(max_length=255, default='')
    text = models.TextField(blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    processed_media_folders = models.ManyToManyField(ProcessedMediaFolder)
