from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin
from .models import *
from modeltranslation.admin import TranslationAdmin
from .forms import CategoryForm

# Register your models here.

# admin.site.register(Category)
admin.site.register(ProductModel)
admin.site.register(GalleryProduct)
admin.site.register(FavoriteProduct)

# admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Profile)


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ("title", "category_icon")
    list_display_links = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    form = CategoryForm

    def category_icon(self, obj):
        if obj.icon:
            try:
                return mark_safe(f'<img src="{obj.icon.url}" >')
            except:
                return 'No icon'
        else:
            return 'No icon'

    category_icon.short_description = 'Иконка'


class GalleryInline(admin.TabularInline):
    model = GalleryProduct
    fk_name = 'product'
    extra = 1


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ('pk', 'title', 'price', 'quantity', 'discount', 'model', 'category', 'product_image')
    list_display_links = ('pk', 'title')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('price', 'discount', 'quantity')
    list_filter = ('discount', 'model', 'category')

    def product_image(self, obj):
        if obj.images:
            try:
                return mark_safe(f'<img src="{obj.images.first().image.url}" width="50">')
            except:
                return 'No icon'
        else:
            return 'No icon'

    product_image.short_description = 'Фото товара'


class SaveOrderProductInline(admin.TabularInline):
    fk_name = 'order'
    model = SaveOrderProduct
    extra = 0
    readonly_fields = ['pk', 'product', 'price', 'color_name', 'product_slug', 'quantity', 'price_in']
    exclude = ['photo']

    def get_photo(self, obj):
        try:
            if obj.photo:
                return mark_safe(f'<img src="{obj.photo}" width="50px">')
            else:
                return '-'
        except:
            return '-'


@admin.register(SaveOrder)
class SaveOrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'customer', 'order_number', 'total_price', 'created_at')
    list_display_links = ('pk', 'customer')
    inlines = [SaveOrderProductInline]


@admin.register(ShippingAddress)
class ShippingAddressAdmin(TranslationAdmin):
    list_display = ('pk', 'customer', 'order', 'phone', 'region', 'city', 'address', 'created_at')
    list_display_links = ('pk', 'customer', 'order')
    list_filter = ('region', 'city', 'created_at')








