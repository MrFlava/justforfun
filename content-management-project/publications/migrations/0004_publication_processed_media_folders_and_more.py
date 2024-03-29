# Generated by Django 4.1.4 on 2022-12-26 14:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processedmediafolders', '0002_processedmediafolder_unzipped_archive_and_more'),
        ('publications', '0003_delete_processedmediafolder_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='processed_media_folders',
            field=models.ManyToManyField(to='processedmediafolders.processedmediafolder'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 26, 14, 24, 29, 539279)),
        ),
        migrations.AlterField(
            model_name='publication',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 26, 14, 24, 29, 539290)),
        ),
    ]
