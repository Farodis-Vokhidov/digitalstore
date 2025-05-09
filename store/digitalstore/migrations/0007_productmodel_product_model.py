# Generated by Django 5.1.6 on 2025-02-16 15:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('digitalstore', '0006_remove_product_brand_remove_product_model_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Модель')),
            ],
            options={
                'verbose_name': 'Модель Товара',
                'verbose_name_plural': 'Модель Товаров',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='digitalstore.productmodel', verbose_name='Модель товара'),
        ),
    ]
