# Generated by Django 4.2.9 on 2024-01-10 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('endpoints', '0002_article_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.URLField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='text',
            field=models.TextField(default=None, null=True),
        ),
    ]
