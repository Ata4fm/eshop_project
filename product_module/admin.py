from django.contrib import admin
from . import models
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['title']
    }
    list_filter = ['category', 'is_active']
    list_display = ['title', 'price', 'is_active', 'is_delete']

admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductCategory)
admin.site.register(models.ProductTag)
admin.site.register(models.ProductAuthor)
admin.site.register(models.ProductVisit)
admin.site.register(models.ProductGallery)


