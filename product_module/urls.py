from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('search/', views.search, name='product-list-search'),
    path('cat/<cat>/', views.ProductListView.as_view(), name='product-categories-list'),
    path('author/<author>/', views.ProductListView.as_view(), name='product-author-list'),
    path('<str:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
]
