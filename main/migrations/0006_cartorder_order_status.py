# Generated by Django 5.0.6 on 2024-06-03 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_cartorder_options_alter_cartorderitems_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='order_status',
            field=models.BooleanField(default=False),
        ),
    ]
