# Generated by Django 3.1 on 2020-10-24 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0014_auto_20201024_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('L', 'liked'), ('P', 'posted'), ('C', 'commented'), ('F', 'followed')], max_length=1),
        ),
    ]
