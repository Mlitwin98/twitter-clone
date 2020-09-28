# Generated by Django 3.1 on 2020-09-28 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=50)),
                ('timeStamp', models.DateTimeField(auto_now=True)),
                ('content', models.TextField()),
            ],
        ),
    ]