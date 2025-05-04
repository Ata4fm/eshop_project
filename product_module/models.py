from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from account_module.models import User


# Create your models here.


class ProductCategory(models.Model):
    title = models.CharField(max_length=300,db_index=True, verbose_name='عنوان')
    url_title = models.CharField(max_length=300,db_index=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی محصولات'

class ProductAuthor(models.Model):
    title = models.CharField(max_length=300,verbose_name='نام نویسنده', db_index=True)
    url_title = models.CharField(max_length=300,verbose_name='نام در url', db_index=True)
    is_active = models.BooleanField(verbose_name='فعال / غیر فعال')


    class Meta:
        verbose_name = 'نویسنده'
        verbose_name_plural = 'نویسندگان'


    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام محصول')
    category = models.ManyToManyField(
        ProductCategory,
        related_name='product_categories'
        ,verbose_name='دسته بندی ها')
    image = models.ImageField(upload_to='images/products', null=True, blank=True, verbose_name='تصویر محصول')
    author = models.ForeignKey(ProductAuthor,on_delete=models.CASCADE,verbose_name='نویسنده', null=True, blank=True)
    price = models.IntegerField(verbose_name='قیمت')
    description = models.TextField(verbose_name='توضیحات اصلی',db_index=True)
    short_description = models.CharField(max_length=500,db_index=True ,null=True, verbose_name='توضیحات کوتاه')
    slug = models.SlugField(default="", null=False, db_index=True, verbose_name='عنولن در url',allow_unicode=True,unique=True, max_length=200)
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')
    page = models.IntegerField(verbose_name='تعداد صفحه',null=True, blank=True)
    print_version = models.IntegerField(verbose_name='نسخه چاپ',null=True, blank=True)

    def get_absolute_url(self):
        return reverse('product-detail', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'



class ProductTag(models.Model):
    caption = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_tags')

    class Meta:
        verbose_name = 'برچسب محصول'
        verbose_name_plural = 'برچسب محصولات'

    def __str__(self):
        return self.caption


class ProductVisit(models.Model):
    product = models.ForeignKey('Product',on_delete=models.CASCADE, verbose_name='محصول')
    ip = models.CharField(max_length=30, verbose_name='آیپی کاربر')
    user = models.ForeignKey(User,null=True, blank=True,verbose_name='کاربر',on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدید های محصول'

    def __str__(self):
        return f'{self.product.title} / {self.ip}'



class ProductGallery(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField(upload_to='images/product-gallery', verbose_name='تصویر')

    class Meta:
        verbose_name = 'گالری تصویر'
        verbose_name_plural = 'گالری تصاویر'

    def __str__(self):
        return self.product.title