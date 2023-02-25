from django.contrib import admin

from note.models import Tag, Entry, Comment


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name', 'slug',)


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_dt', 'updated_dt',)
    list_filter = ('created_dt', 'updated_dt',)
    search_fields = ('title', 'body',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'entry', 'created_dt', 'updated_dt',)
    list_filter = ('created_dt', 'updated_dt',)
    search_fields = ('body',)
