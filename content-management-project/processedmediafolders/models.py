from datetime import datetime

from django.db import models


class UnzippedArchive(models.Model):
    archive_name = models.CharField(max_length=50, default='')


class ProcessedMediaFolder(models.Model):
    name = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(default=datetime.now())
    updated_at = models.DateTimeField(default=datetime.now())
    is_pdf_moved = models.BooleanField(default=False)
    is_image_converted = models.BooleanField(default=False)
    is_audio_converted = models.BooleanField(default=False)
    is_video_converted = models.BooleanField(default=False)
    is_multipage_pdfs_splitted = models.BooleanField(default=False)
    is_name_corrected = models.BooleanField(default=False)
    is_pdf_converted = models.BooleanField(default=False)
    is_video_posters_created = models.BooleanField(default=False)
    is_image_pushed_to_s3 = models.BooleanField(default=False)
    is_audio_pushed_to_s3 = models.BooleanField(default=False)
    is_video_pushed_to_s3 = models.BooleanField(default=False)
    is_multipage_pdf_pushed_to_s3 = models.BooleanField(default=False)
    is_singlepage_pdf_pushed_to_s3 = models.BooleanField(default=False)
    unzipped_archive = models.ForeignKey(UnzippedArchive, on_delete=models.CASCADE)
