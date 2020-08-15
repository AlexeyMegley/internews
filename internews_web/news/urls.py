from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.main),
    path("country/<int:country_id>/", views.main),
    path("country/<int:country_id>/media/<int:media_id>/", views.main),
]
