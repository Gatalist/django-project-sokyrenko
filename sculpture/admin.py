from django.contrib import admin

from .models import Category, Author, Sculpture, ImageSculpture, Reviews, ImageHome, News, Development, ImageDevelopment, PlaceOder


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("name",)


@admin.register(Sculpture)
class SculptureAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "url", "draft")
    list_display_links = ("title",)
    save_as = True
    save_on_top = True
    list_editable = ("draft", )


@admin.register(ImageSculpture)
class SculptureAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "sculpture")
    list_display_links = ("title",)


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "sculpture", "year")
    list_display_links = ("name",)


@admin.register(ImageHome)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ("id", "sculpture")
    list_display_links = ("sculpture",)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "year")
    list_display_links = ("title",)


@admin.register(Development)
class DevelopmentAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "url")
    list_display_links = ("title",)


@admin.register(ImageDevelopment)
class ImageDevelopmentAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "sculpture")
    list_display_links = ("title",)


@admin.register(PlaceOder)
class PlaceOderAdmin(admin.ModelAdmin):
    list_display = ("id", "year", "first_name", "phone", "sculpture")
    list_display_links = ("first_name",)
