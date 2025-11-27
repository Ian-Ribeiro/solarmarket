from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls')),
    path('marketplace/', include('marketplace.urls')),
    path('orders/', include('orders.urls')),
    path('installers/', include('installers.urls')),
    path('quotes/', include('quotes.urls')),
    path('reviews/', include('reviews.urls')),
    path('dashboard/', include('dashboard.urls')),
]