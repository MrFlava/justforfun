from django.contrib import admin

from processedmediafolders.models import ProcessedMediaFolder, UnzippedArchive


@admin.register(ProcessedMediaFolder)
class ProcessedMediaFolderAdmin(admin.ModelAdmin):
    pass


@admin.register(UnzippedArchive)
class UnzippedArchiveAdmin(admin.ModelAdmin):
    pass
