# Generated by Django 5.2 on 2025-05-20 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorials', '0024_tutorialsection_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutorialsection',
            name='video',
        ),
        migrations.AlterField(
            model_name='tutorialsection',
            name='image',
            field=models.FileField(blank=True, help_text='(optional) Bild- oder Videodatei', null=True, upload_to='tutorial_images/'),
        ),
    ]
