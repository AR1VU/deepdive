# Generated by Django 5.1.7 on 2025-04-22 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_generator', '0002_customuser_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='name',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
    ]
