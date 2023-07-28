# Generated by Django 4.2.3 on 2023-07-28 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_alter_ingredient_options_alter_menuitem_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(choices=[('GR', 'Grams'), ('KG', 'Kilograms'), ('ML', 'Mililitres'), ('LI', 'Litres'), ('NU', 'Number'), ('TS', 'Teaspoon'), ('TB', 'Tablespoon')], help_text='Please choose a unit of measurement from the available options.', max_length=2),
        ),
    ]
