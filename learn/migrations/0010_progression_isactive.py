# Generated by Django 2.1.5 on 2019-03-12 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0009_remove_usercustom_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='progression',
            name='IsActive',
            field=models.BooleanField(default=True, max_length=20),
        ),
    ]
