from django.contrib import admin

from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'content',
        'writer',
        'created',
        'deleted',
    )
    search_fields = ('post__title', 'content', 'writer__user_id',)

admin.site.register(Comment, CommentAdmin)
