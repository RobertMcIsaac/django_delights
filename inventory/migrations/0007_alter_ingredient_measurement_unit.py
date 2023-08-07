# Generated by Django 4.2.3 on 2023-08-07 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_rename_ingredient_quantity_required_reciperequirement_ingredient_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(choices=[('GR', 'g (Grams)'), ('KG', 'Kg (Kilograms)'), ('ML', 'ml (Mililitres)'), ('LI', 'L (Litres)'), ('NU', 'Number'), ('TS', 'Tsp (Teaspoon)'), ('TB', 'Tbsp (Tablespoon)')], help_text='Please choose a unit of measurement from the available options.', max_length=2),
        ),
    ]