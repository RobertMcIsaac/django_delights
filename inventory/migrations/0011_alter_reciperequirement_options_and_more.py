# Generated by Django 4.2.3 on 2023-08-08 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_alter_ingredient_measurement_unit'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reciperequirement',
            options={'ordering': ['menuitem'], 'verbose_name': 'Recipe requirement'},
        ),
        migrations.RenameField(
            model_name='purchase',
            old_name='menu_item',
            new_name='menuitem',
        ),
        migrations.RenameField(
            model_name='reciperequirement',
            old_name='menu_item',
            new_name='menuitem',
        ),
    ]
