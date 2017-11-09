from django.contrib import admin

from backend.models import Portal, Comment, Tag, TagType


class TagInline(admin.StackedInline):
    model = Tag


class PortalInline(admin.StackedInline):
    model = Portal


@admin.register(Portal)
class PortalModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'nickname', 'link']
    list_display_links = ['title']
    list_filter = ['tags']
    search_fields = ['title', 'nickname']
    list_per_page = 20
    readonly_fields = ['image', 'late6', 'lnge6']
    fieldsets = [
        ('', {'fields': ['title', 'nickname', 'link', 'image']}),
        ('Location', {'fields': ['late6', 'lnge6']}),
        ('Rel', {'fields': ['author', 'tags', 'adder']})
    ]


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    pass


@admin.register(TagType)
class TagTypeModelAdmin(admin.ModelAdmin):
    pass
