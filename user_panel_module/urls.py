from django.urls import path
from . import views
urlpatterns = [
    path('',views.UserPanelDashboardPage.as_view(),name='user-panel-dashboard'),
    path('edit-profile', views.EditUserProfilePage.as_view(), name='edit-profile'),
    path('user-favorite', views.UserFavoriteCategories.as_view(), name='user-favorite-category'),
    path('change-password', views.ChangePasswordPage.as_view(), name='change-password'),
    path('user-basket', views.user_basket, name='user-basket'),
    path('remove-order-detail', views.remove_order_detail, name='remove-order-detail'),
    path('my-shopping', views.myShopping.as_view(), name='my-shopping'),
    path('my-shopping-detail/<order_id>', views.my_shopping_detail, name='my-shopping-detail'),
    path('change-order-detail', views.change_order_detail_count, name='change-order-detail'),


]