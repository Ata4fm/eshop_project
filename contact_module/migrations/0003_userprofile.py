# Generated by Django 4.1.3 on 2022-12-07 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact_module', '0002_alter_contactus_is_read_by_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='images')),
            ],
        ),
    ]
