from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


DEFAULT_AVATAR_URL = "https://www.w3schools.com/howto/img_avatar.png"


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название категории')
    icon = models.ImageField(upload_to='icons/', verbose_name='Иконка категории', null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, verbose_name='Слаг категории')

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def get_icon(self):
        if self.icon:
            return self.icon.url
        else:
            return '@'


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название продукта")
    price = models.FloatField(verbose_name="Цена товара")
    quantity = models.IntegerField(default=0, verbose_name="Количество товара")
    color_name = models.CharField(max_length=20, default="Белый", verbose_name="Название цвета")
    color_code = models.CharField(max_length=20, default="#ffffff", verbose_name="Код цвета")
    slug = models.SlugField(unique=True, null=True, verbose_name="Слаг товара")
    discount = models.IntegerField(null=True, blank=True, verbose_name="Скидка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products",
                                 verbose_name="Категория")
    model = models.ForeignKey('ProductModel', on_delete=models.CASCADE, verbose_name='Модель товара', null=True, blank=True)
    release_date = models.CharField(max_length=50, verbose_name="Дата выхода", null=True, blank=True)
    dimensions = models.CharField(max_length=100, verbose_name="Размеры (ВxШxГ)", null=True, blank=True)
    weight = models.FloatField(verbose_name="Вес (г, кг)", null=True, blank=True)
    material = models.CharField(max_length=100, verbose_name="Материал корпуса", null=True, blank=True)
    battery = models.CharField(max_length=100, verbose_name="Ёмкость аккумулятора", null=True, blank=True)
    screen_technology = models.CharField(max_length=100, verbose_name="Технология экрана", null=True, blank=True)
    screen_size = models.CharField(max_length=50, verbose_name="Размер экрана (диагональ)", null=True, blank=True)
    main_camera = models.CharField(max_length=100, verbose_name="Основная камера", null=True, blank=True)
    front_camera = models.CharField(max_length=100, verbose_name="Фронтальная камера", null=True, blank=True)
    operating_system = models.CharField(max_length=100, verbose_name="Операционная система", null=True, blank=True)
    guarantee = models.CharField(max_length=50, verbose_name='Гарантия', null=True, blank=True)
    tv_resolution = models.CharField(max_length=50, verbose_name="Разрешение экрана", null=True, blank=True)
    tv_smart = models.CharField(max_length=20, null=True, blank=True, verbose_name="Smart TV")
    tv_refresh_rate = models.CharField(max_length=50, verbose_name="Частота обновления", null=True, blank=True)
    fridge_capacity = models.CharField(max_length=50, verbose_name="Объем холодильной камеры (л)", null=True,
                                       blank=True)
    freezer_capacity = models.CharField(max_length=50, verbose_name="Объем морозильной камеры (л)", null=True,
                                        blank=True)
    energy_class = models.CharField(max_length=20, verbose_name="Класс энергопотребления", null=True, blank=True)
    fridge_compressor_type = models.CharField(max_length=50, verbose_name="Тип компрессора", null=True, blank=True)
    ac_cooling_power = models.CharField(max_length=50, verbose_name="Мощность охлаждения", null=True, blank=True)
    coverage_area = models.CharField(max_length=50, verbose_name="Площадь размещения", null=True, blank=True)
    maximum_temperature = models.CharField(max_length=50, verbose_name="Максимальная температура", null=True, blank=True)
    minimum_temperature = models.CharField(max_length=50, verbose_name="Минимальная температура", null=True, blank=True)
    ac_heating_power = models.CharField(max_length=50, verbose_name="Мощность обогрева", null=True, blank=True)
    ac_noise_level = models.CharField(max_length=50, verbose_name="Уровень шума", null=True, blank=True)

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def get_price(self):
        if self.discount:
            desc = self.price * self.discount / 100
            new_price = self.price - desc
            return new_price
        else:
            return self.price

    def get_first_photo(self):
        if self.images:
            try:
                return self.images.first().image.url
            except:
                return '-'
        else:
            return '-'


class GalleryProduct(models.Model):
    image = models.ImageField(upload_to='products/', verbose_name='Фото товара')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', related_name='images')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Фото Товара'
        verbose_name_plural = 'Фото Товаров'


class ProductModel(models.Model):
    title = models.CharField(max_length=150, verbose_name='Модель')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Модель Товара'
        verbose_name_plural = 'Модель Товаров'


class FavoriteProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return f'Товар {self.product.title} пользователя {self.user.username}'

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')
    region = models.CharField(max_length=150, verbose_name='Регион', blank=True, null=True)
    city = models.CharField(max_length=150, verbose_name='Город', blank=True, null=True)
    street = models.CharField(max_length=150, verbose_name='Улица', blank=True, null=True)
    home = models.CharField(max_length=150, verbose_name='Дом', blank=True, null=True)
    flat = models.CharField(max_length=150, verbose_name='№ Квартиры', blank=True, null=True)
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона', blank=True, null=True)

    def __str__(self):
        return f'Покупатель {self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Покупатель')
    is_completed = models.BooleanField(default=False, verbose_name='Статус заказа')
    payment = models.BooleanField(default=False, verbose_name='Статус оплаты')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата начала заказа')
    shipping = models.BooleanField(default=True, verbose_name='Доставка')

    def __str__(self):
        return f'Заказ покупателя {self.customer.user.first_name} по № {self.pk}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    @property
    def get_order_total_price(self):
        order_products = self.orderproduct_set.all()
        total_price = sum([i.get_total_price for i in order_products])
        return total_price

    @property
    def get_order_total_quantity(self):
        order_products = self.orderproduct_set.all()
        total_quantity = sum([i.quantity for i in order_products])
        return total_quantity


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    @property
    def get_total_price(self):
        return self.quantity * self.product.get_price()

    def old_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f'Товар {self.product.title} для заказа № {self.order.pk}'

    class Meta:
        verbose_name = 'Товар в заказ'
        verbose_name_plural = 'Товары заказов'


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Покупатель')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    phone = models.CharField(max_length=50, verbose_name='Номер телефона')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата оформления')
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True, max_length=200)
    address = models.TextField(max_length=150, verbose_name='Адрес', null=True, blank=True)
    region = models.TextField(max_length=100, verbose_name='Регион доставки')
    city = models.TextField(max_length=100, verbose_name='Город доставки')

    def __str__(self):
        return f'Доставка на имя {self.customer.user.first_name} по заказу №:{self.order.pk}'

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставок'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='profile_avatars/', blank=True, null=True, verbose_name="Аватар")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Номер телефона")

    def get_image_url(self):
        if self.image:
            return self.image.url
        return DEFAULT_AVATAR_URL

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class SaveOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, verbose_name='Покупатель', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    total_price = models.FloatField(default=0, verbose_name='Сумма заказа')
    order_number = models.IntegerField(verbose_name='Номер заказа')
    completed = models.BooleanField(default=False, verbose_name='Статус заказа')

    def __str__(self):
        return f'Заказ №: {self.pk} на пользователя {self.customer.user.username}'

    class Meta:
        verbose_name = 'Сохранить заказ'
        verbose_name_plural = 'Сохраннёные заказы'


class SaveOrderProduct(models.Model):
    order = models.ForeignKey(SaveOrder, on_delete=models.CASCADE, related_name='products')
    product = models.CharField(max_length=300, verbose_name='Название товара')
    quantity = models.IntegerField(default=0, verbose_name='Кол-во')
    price = models.FloatField(default=0, verbose_name='Цена товара')
    product_slug = models.CharField(max_length=300, verbose_name='Слаг товара')
    price_in = models.FloatField(verbose_name='На сумму')
    photo = models.ImageField(upload_to='images/', verbose_name='Фото товара')
    color_name = models.CharField(max_length=100, verbose_name='Название товара')

    def __str__(self):
        return f'Товар {self.product} заказа № {self.order.pk}'

    class Meta:
        verbose_name = 'Сохранить товар в заказ'
        verbose_name_plural = 'Сохраннёные товары заказы '
















