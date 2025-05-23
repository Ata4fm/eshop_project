# Generated by Django 4.1.3 on 2022-11-26 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='id_delete',
            new_name='is_delete',
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(allow_unicode=True, default='', max_length=200, unique=True, verbose_name='عنولن در url'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=300, verbose_name='نام محصول'),
        ),
    ]
