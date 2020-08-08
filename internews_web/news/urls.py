from django.urls import include, path
from . import views

urlpatterns = [
    path('1/', views.russia),
    path('2/', views.usa),
]
