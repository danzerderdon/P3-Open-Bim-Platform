# Generated by Django 5.2 on 2025-04-29 08:58

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorials', '0020_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeinModell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', ckeditor.fields.RichTextField()),
            ],
        ),
        migrations.AlterField(
            model_name='tutorialsection',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
