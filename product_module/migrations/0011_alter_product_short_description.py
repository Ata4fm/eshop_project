# Generated by Django 4.1.4 on 2022-12-18 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0010_product_page_product_print_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='short_description',
            field=models.CharField(db_index=True, max_length=500, null=True, verbose_name='توضیحات کوتاه'),
        ),
    ]
