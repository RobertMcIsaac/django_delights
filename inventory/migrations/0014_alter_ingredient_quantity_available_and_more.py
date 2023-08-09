# Generated by Django 4.2.3 on 2023-08-09 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_alter_ingredient_measurement_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='quantity_available',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='reciperequirement',
            name='ingredient_quantity',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=6),
        ),
    ]
