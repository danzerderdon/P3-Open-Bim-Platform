# Generated by Django 5.2 on 2025-05-20 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorials', '0025_remove_tutorialsection_video_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutorialsection',
            name='video',
            field=models.FileField(blank=True, help_text='(optional) MP4, WebM oder Ogg', null=True, upload_to='tutorial_images/'),
        ),
        migrations.AlterField(
            model_name='tutorialsection',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='tutorial_images/'),
        ),
    ]
