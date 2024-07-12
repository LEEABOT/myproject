# Generated by Django 5.0.2 on 2024-03-01 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foodname', models.CharField(max_length=255)),
                ('picsrc', models.CharField(max_length=255)),
                ('foodmaterial', models.TextField()),
                ('foodstep', models.TextField()),
            ],
        ),
    ]
