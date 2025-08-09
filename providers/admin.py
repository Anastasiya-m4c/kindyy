"""
Admin configuration for the blog application's Post model.

Uses django-summernote for rich text editing of the content field.
"""

from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    """
    Admin interface customization for the Post model.

    Enables rich text editing on the content field and provides
    search, filter, and slug prepopulation features.
    """
    list_display = ('title', 'slug', 'status')
    search_fields = ['title']
    list_filter = ('status',)
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)
