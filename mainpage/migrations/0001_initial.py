# Generated by Django 5.0.2 on 2024-02-23 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='userInfo',
            fields=[
                ('user_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=20)),
                ('user_password', models.CharField(max_length=20)),
            ],
        ),
    ]
