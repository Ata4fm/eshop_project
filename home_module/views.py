from itertools import product

from django.db.models import Count, Sum
from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic.base import TemplateView

from product_module.models import Product, ProductCategory
from site_module.models import SiteSetting, FooterLinkBox, Slider
from utils.convertors import group_list
from account_module.models import User

class HomeView(TemplateView):
    template_name = 'home_module/index_page.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sliders = Slider.objects.filter(is_active=True)
        context['sliders'] = sliders
        latest_products = Product.objects.filter(is_active=True, is_delete=False).order_by('-id')[:12]
        most_visit_products = Product.objects.filter(is_active=True, is_delete=False).annotate(
            visit_count=Count('productvisit')).order_by('-visit_count')[:12]
        context['latest_products'] = group_list(latest_products)
        context['most_visit_products'] = group_list(most_visit_products)
        categories = list(
            ProductCategory.objects.annotate(products_count=Count('product_categories')).filter(is_active=True,is_delete=False,products_count__gt=0)[:6])
        categories_products = []
        for category in categories:
            item = {
                'id': category.id,
                'title': category.title,
                'url_title': category.url_title,
                'products': list(category.product_categories.all()[:4])
            }
            categories_products.append(item)

        context['categories_products'] = categories_products
        most_bought_products = Product.objects.filter(orderdetail__order__is_paid=True).annotate(order_count=Sum(
            'orderdetail__count'
        )).order_by('-order_count')[:12]
        context['most_bought_products'] = group_list(most_bought_products)

        fav_categories = list()
        user_profile = User.objects.filter(id=self.request.user.id).first()
        if user_profile:
            for cat in user_profile.favorite.all():
                products = Product.objects.filter(category=cat)
                if products.exists():
                    fav_categories.append(products)

            context['fav_categories'] = fav_categories
        return context


class AboutView(TemplateView):
    template_name = 'home_module/about_page.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        site_setting = SiteSetting.objects.filter(is_main_setting=True).first()
        context['site_setting'] = site_setting
        return context






def site_header_component(request):
    serach_query = ''
    if request.GET.get('q'):
        serach_query = request.GET.get('q')
    setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    context = {
        'site_setting': setting,
        'search_query': serach_query


    }
    return render(request, 'shared/site_header.html', context)


def site_footer_component(request):
    setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    footer_link_boxes = FooterLinkBox.objects.all()
    for item in footer_link_boxes:
        item.footerlink_set
    context = {
        'site_setting': setting,
        'footer_link_boxes': footer_link_boxes
    }
    return render(request, 'shared/site_footer.html', context)


