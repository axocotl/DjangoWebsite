from django.contrib import admin
from .models import Comment, Author


class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 3


# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['author_id', 'small_avatar_url', 'username']})
    ]
    inlines = [CommentInLine]
    list_display = ('author_id', 'small_avatar_url', 'username')


admin.site.register(Author, AuthorAdmin)