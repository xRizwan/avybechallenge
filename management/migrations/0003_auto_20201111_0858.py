# Generated by Django 3.0.8 on 2020-11-11 03:58

from django.db import migrations, models
import management.models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_auto_20201110_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(upload_to=management.models.user_directory_path),
        ),
    ]