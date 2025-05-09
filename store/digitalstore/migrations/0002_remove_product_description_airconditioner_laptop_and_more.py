# Generated by Django 5.1.6 on 2025-02-14 05:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digitalstore', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.CreateModel(
            name='AirConditioner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(verbose_name='Дата выхода')),
                ('cooling_capacity', models.CharField(max_length=50, verbose_name='Мощность охлаждения')),
                ('power_consumption', models.CharField(max_length=50, verbose_name='Энергопотребление')),
                ('noise_level', models.CharField(max_length=50, verbose_name='Уровень шума')),
                ('modes', models.TextField(verbose_name='Режимы (Охлаждение, Обогрев, Осушение, Вентиляция)')),
                ('filter_type', models.CharField(max_length=100, verbose_name='Тип фильтра')),
                ('dimensions', models.CharField(max_length=100, verbose_name='Размеры (ШxВxГ)')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='digitalstore.product')),
            ],
            options={
                'verbose_name': 'Кондиционер',
                'verbose_name_plural': 'Кондиционеры',
            },
        ),
        migrations.CreateModel(
            name='Laptop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(verbose_name='Дата выхода')),
                ('dimensions', models.CharField(max_length=100, verbose_name='Размеры (ШxВxГ)')),
                ('processor', models.CharField(max_length=100, verbose_name='Процессор')),
                ('ram', models.CharField(max_length=50, verbose_name='ОЗУ')),
                ('storage', models.CharField(max_length=50, verbose_name='Накопитель')),
                ('screen_size', models.CharField(max_length=20, verbose_name='Размер экрана')),
                ('screen_resolution', models.CharField(max_length=50, verbose_name='Разрешение экрана')),
                ('battery', models.CharField(max_length=100, verbose_name='Аккумулятор')),
                ('os', models.CharField(max_length=50, verbose_name='Операционная система')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='digitalstore.product')),
            ],
            options={
                'verbose_name': 'Ноутбук',
                'verbose_name_plural': 'Ноутбуки',
            },
        ),
        migrations.CreateModel(
            name='Refrigerator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dimensions', models.CharField(max_length=100, verbose_name='Размеры (ШxВxГ)')),
                ('capacity', models.CharField(max_length=100, verbose_name='Общий объем')),
                ('energy_class', models.CharField(max_length=10, verbose_name='Класс энергопотребления')),
                ('defrosting', models.CharField(max_length=50, verbose_name='Тип разморозки')),
                ('number_of_doors', models.IntegerField(verbose_name='Количество дверей')),
                ('cooling_technology', models.CharField(max_length=100, verbose_name='Технология охлаждения')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='digitalstore.product')),
            ],
            options={
                'verbose_name': 'Холодильник',
                'verbose_name_plural': 'Холодильники',
            },
        ),
        migrations.CreateModel(
            name='Smartphone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(verbose_name='Дата выхода')),
                ('dimensions', models.CharField(max_length=100, verbose_name='Размеры (ВxШxГ)')),
                ('body_material', models.CharField(max_length=100, verbose_name='Корпуса')),
                ('battery_capacity', models.CharField(max_length=50, verbose_name='Аккумулятор')),
                ('display_technology', models.CharField(max_length=50, verbose_name='Тип экрана')),
                ('screen_size', models.CharField(max_length=20, verbose_name='Диагональ экрана')),
                ('resolution', models.CharField(max_length=50, verbose_name='Разрешение экрана')),
                ('refresh_rate', models.CharField(max_length=10, verbose_name='Частота обновления')),
                ('main_camera', models.CharField(max_length=100, verbose_name='Основная камера')),
                ('front_camera', models.CharField(max_length=100, verbose_name='Фронтальная камера')),
                ('os', models.CharField(max_length=50, verbose_name='Операционная система')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='digitalstore.product')),
            ],
        ),
        migrations.CreateModel(
            name='TV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(verbose_name='Дата выхода')),
                ('dimensions', models.CharField(max_length=100, verbose_name='Размеры (ШxВxГ)')),
                ('screen_type', models.CharField(max_length=50, verbose_name='Тип экрана')),
                ('resolution', models.CharField(max_length=50, verbose_name='Разрешение')),
                ('refresh_rate', models.CharField(max_length=10, verbose_name='Частота обновления')),
                ('sound', models.CharField(max_length=100, verbose_name='Звук')),
                ('smart_tv', models.BooleanField(default=True, verbose_name='Smart TV')),
                ('ports', models.TextField(verbose_name='Порты (HDMI, USB, Bluetooth, Wi-Fi)')),
                ('power_consumption', models.CharField(max_length=50, verbose_name='Энергопотребление')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='digitalstore.product')),
            ],
            options={
                'verbose_name': 'Телевизор',
                'verbose_name_plural': 'Телевизоры',
            },
        ),
    ]
