# Generated by Django 4.2.3 on 2023-08-09 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_alter_ingredient_quantity_available_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='cost_per_unit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='quantity_available',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='reciperequirement',
            name='ingredient_quantity',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]