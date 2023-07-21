from django.contrib import admin

from publications.models import Publication, Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    pass
