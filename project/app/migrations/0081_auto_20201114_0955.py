# Generated by Django 3.1.2 on 2020-11-14 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0080_auto_20201114_0923'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HoDanDoQuanTrong',
        ),
        migrations.DeleteModel(
            name='HoDanLienLac',
        ),
        migrations.DeleteModel(
            name='HoDanNhuCau',
        )
    ]
