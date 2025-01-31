# Generated by Django 5.0.6 on 2024-05-17 17:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Banner",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("banner_img", models.ImageField(upload_to="banner_images/")),
                ("banner_alt_text", models.CharField(max_length=300)),
            ],
            options={
                "verbose_name_plural": "1. Banners",
            },
        ),
        migrations.CreateModel(
            name="ProductCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("category_name", models.CharField(max_length=100)),
                ("image", models.ImageField(upload_to="product_category_images/")),
            ],
            options={
                "verbose_name_plural": "2. Products Categories",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("product_name", models.CharField(max_length=200)),
                ("image", models.ImageField(upload_to="products_images/")),
                ("slug", models.CharField(max_length=400)),
                ("details", models.TextField()),
                ("available", models.BooleanField(default=True)),
                ("is_featured", models.BooleanField(default=False)),
                (
                    "product_category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="main.productcategory",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "3. Products",
            },
        ),
    ]
