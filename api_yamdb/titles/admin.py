from django.contrib import admin

from titles.models import Category, Title, Genre, TitleGenre


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'raiting', 'description',
                    'category')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')


class TitleGenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'genre')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(TitleGenre, TitleGenreAdmin)
