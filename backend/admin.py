from django.contrib import admin

from backend.models import Portal, Comment, Tag


@admin.register(Portal)
class PortalModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    pass
