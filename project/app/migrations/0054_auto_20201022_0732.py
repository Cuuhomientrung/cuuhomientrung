# Generated by Django 3.1.2 on 2020-10-22 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0053_auto_20201022_0628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hodan',
            name='people_number',
            field=models.PositiveIntegerField(blank=True, default=1, null=True, verbose_name='Số người'),
        ),
    ]
