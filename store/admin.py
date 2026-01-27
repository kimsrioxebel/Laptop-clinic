# # # # from django.contrib import admin

# # # # # Register your models here.
# # # from django.contrib import admin
# # # from .models import Laptop

# # # @admin.register(Laptop)
# # # class LaptopAdmin(admin.ModelAdmin):
# # #     list_display = ('brand', 'model_name', 'price', 'ram', 'storage', 'stock')
# # #     search_fields = ('brand', 'model_name', 'processor')
# # #     list_filter = ('brand', 'ram', 'storage')
# # from django.contrib import admin
# # from .models import Laptop, Brand, Category

# # @admin.register(Brand)
# # class BrandAdmin(admin.ModelAdmin):
# #     search_fields = ('name',)


# # @admin.register(Category)
# # class CategoryAdmin(admin.ModelAdmin):
# #     search_fields = ('name',)


# # @admin.register(Laptop)
# # class LaptopAdmin(admin.ModelAdmin):
# #     list_display = ('brand', 'model_name', 'category', 'price', 'stock')
# #     list_filter = ('brand', 'category')
# #     search_fields = ('model_name', 'processor')
# from django.contrib import admin
# from .models import Laptop, Brand, Category


# @admin.register(Brand)
# class BrandAdmin(admin.ModelAdmin):
#     search_fields = ('name',)


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     search_fields = ('name',)


# @admin.register(Laptop)
# class LaptopAdmin(admin.ModelAdmin):
#     list_display = ('brand', 'model_name', 'category', 'price', 'stock')
#     list_filter = ('brand', 'category')
#     search_fields = ('model_name', 'processor')
from django.contrib import admin
from .models import Brand, Category, Laptop


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Laptop)
class LaptopAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'model_name',
        'brand',
        'category',
        'price',
        'stock',
        'created_at',
    )
    list_filter = ('brand', 'category')
    search_fields = ('model_name', 'processor', 'ram', 'storage')
