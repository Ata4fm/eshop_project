# Generated by Django 4.1.4 on 2022-12-14 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0002_remove_user_mobile_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.TextField(blank=True, null=True, verbose_name='آدرس'),
        ),
    ]
