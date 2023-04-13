from django.contrib import admin
from django.urls import path, include
from . import views
from accounts.views import add_to_read, save_coin_amount

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),  # Add the namespace here
    path('accounts/add_to_read/<int:article_id>/', add_to_read, name='add_to_read'),
    path('accounts/save_coin_amount/<str:coin_id>/', save_coin_amount, name='save_coin_amount'),
    ]

