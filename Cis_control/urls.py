from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('controls_list/', views.controls_list, name='controls list'),

    # path('', include(router.urls)),
    # path('tool/', views.ToolViewSet.as_view(), name='tool'),
]
