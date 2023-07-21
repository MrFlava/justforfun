# Generated by Django 4.1.4 on 2022-12-26 14:24

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('processedmediafolders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='processedmediafolder',
            name='unzipped_archive',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='processedmediafolders.unzippedarchive'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='processedmediafolder',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 26, 14, 24, 29, 538623)),
        ),
        migrations.AlterField(
            model_name='processedmediafolder',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 26, 14, 24, 29, 538635)),
        ),
        migrations.AlterField(
            model_name='unzippedarchive',
            name='archive_name',
            field=models.CharField(default='', max_length=50),
        ),
    ]
