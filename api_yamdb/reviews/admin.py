from django.contrib import admin

from reviews.models import Comments, Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'score', 'pub_date', 'title')


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'pub_date', 'review')


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comments, CommentsAdmin)
