from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from site_module.models import SiteBanner
from .models import Product, ProductCategory, ProductAuthor, ProductVisit, ProductGallery
from utils.http_service import get_client_ip
from utils.convertors import group_list
from .utils import searchProducts


def search(request):
    products , searched = searchProducts(request)

    page = request.GET.get('page')
    results = 9
    paginator = Paginator(products,results)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        products = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        products = paginator.page(page)


    return render(request, 'product_module/search.html', {
        'searched': searched,
        'products': products,
        'paginator': paginator
    })





class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product
    context_object_name = 'products'
    ordering = ['price']
    paginate_by = 9

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super(ProductListView, self).get_context_data()
        query = Product.objects.all()
        product: Product = query.order_by('-price').first()
        db_max_price = product.price if product is not None else 0
        context['db_max_price'] = db_max_price
        context['start_price'] = self.request.GET.get('start_price') or 0
        context['end_price'] = self.request.GET.get('end_price') or db_max_price
        context['banners'] = SiteBanner.objects.filter(is_active=True,positions__iexact=SiteBanner.SiteBannerPositions.product_list)
        return context

    def get_queryset(self):
        query = super(ProductListView, self).get_queryset()
        category_name = self.kwargs.get('cat')
        author_name = self.kwargs.get('author')
        request: HttpRequest = self.request
        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')
        if start_price is not None:
            query = query.filter(price__gte=start_price)
        if end_price is not None:
            query = query.filter(price__lte=end_price)

        if author_name is not None:
            query = query.filter(author__url_title__iexact=author_name)

        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)
        return query


class ProductDetailView(DetailView):
    template_name = 'product_module/product_detail.html'
    model = Product


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_product = self.object
        context['banners'] = SiteBanner.objects.filter(is_active=True,positions__iexact=SiteBanner.SiteBannerPositions.product_detail)
        galleries = list(ProductGallery.objects.filter(product_id=loaded_product.id).all())
        galleries.insert(0, loaded_product)
        context['product_galleries_group'] = group_list(galleries, 3)
        context['related_products'] = group_list(list(Product.objects.filter(author_id=loaded_product.author_id).exclude(pk=loaded_product.id).all()[:12]), 3)
        user_ip = get_client_ip(self.request)
        user_id = None

        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip,product_id=loaded_product.id).exists()

        if not has_been_visited:
            new_visit = ProductVisit(ip=user_ip, user_id=user_id, product_id=loaded_product.id)
            new_visit.save()

        return context




def product_categories_component(request: HttpRequest):
    product_categories = ProductCategory.objects.filter(is_active=True, is_delete=False)
    context = {
        'categories': product_categories
    }
    return render(request, 'product_module/components/product_categories.html', context)


def books_author_component(request: HttpRequest):
    books_author = ProductAuthor.objects.annotate(products_count=Count('product')).filter(is_active=True)
    context = {
        'authors': books_author
    }
    return render(request, 'product_module/components/product_author.html', context)
