# Generated by Django 4.2.3 on 2023-08-28 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0020_ingredient_created_at_menuitem_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
