# Generated by Django 2.1.5 on 2019-01-23 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0002_auto_20190123_1318'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='word',
            name='Phonetics',
        ),
        migrations.AddField(
            model_name='wordjp',
            name='Phonetics',
            field=models.CharField(default=None, max_length=20),
            preserve_default=False,
        ),
    ]
