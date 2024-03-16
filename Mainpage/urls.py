from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('auctions/', include(('auctions.urls', 'auctions'), namespace='auctions')),
    path('Dashboard/', include(('Dashboard.urls', 'auctions'), namespace='Dashboard')),
]