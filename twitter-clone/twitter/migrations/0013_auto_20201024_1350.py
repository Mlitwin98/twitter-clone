# Generated by Django 3.1 on 2020-10-24 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0012_auto_20201024_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='author',
            field=models.CharField(max_length=50),
        ),
    ]