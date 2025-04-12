from modeltranslation.translator import register, TranslationOptions
from .models import *


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'color_name', 'material', 'operating_system', 'guarantee',
              'tv_resolution', 'tv_smart', 'tv_refresh_rate', 'fridge_compressor_type',
              'energy_class', 'ac_cooling_power', 'ac_heating_power', 'ac_noise_level',
              'screen_technology', 'main_camera', 'front_camera')


@register(ProductModel)
class ProductModelTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(SaveOrderProduct)
class SaveOrderProductTranslationOptions(TranslationOptions):
    fields = ('product', 'color_name')


@register(ShippingAddress)
class ShippingAddressTranslationOptions(TranslationOptions):
    fields = ('comment', 'address', 'region', 'city')





























