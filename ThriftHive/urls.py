"""
URL configuration for ThriftHive project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from ThriftHive import settings
from store.views import add_to_cart, cart, create_store, delete_item, home, create_item, item_view, login_view, logout_view, order, register_view, store_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('category/<str:category>/', home, name="category_home"),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('create_item/', create_item, name="create_item"),
    path('delete_item/<int:id>', delete_item, name="delete_item"),
    path('create_store/', create_store, name="create_store"),
    path('store/<str:username>/', store_view, name='store_view'),
    path('view/<int:id>', item_view, name='item_view'),
    path('cart/', cart, name='cart'),
    path('add_to_cart/<int:id>', add_to_cart, name='add_to_cart'),
    path('order/', order, name='order')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
