# Generated by Django 4.2.4 on 2023-08-28 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_item_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(blank=True, choices=[('new', 'new'), ('sale', 'sale')], max_length=10, null=True),
        ),
    ]