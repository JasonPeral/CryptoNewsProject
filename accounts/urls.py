from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('list/', views.list, name='list'),
    path('save_coin_amount/<str:coin_id>/', views.save_coin_amount, name='save_coin_amount'),
    path('delete_coin_amount/<int:coin_amount_id>/', views.delete_coin_amount, name='delete_coin_amount'),
    path('delete_from_read/<int:article_id>/', views.delete_from_read, name='delete_from_read')
]
