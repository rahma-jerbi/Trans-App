# Generated by Django 4.2.11 on 2024-05-03 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transcription', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transcription',
            name='transcribed_text',
            field=models.TextField(blank=True),
        ),
    ]