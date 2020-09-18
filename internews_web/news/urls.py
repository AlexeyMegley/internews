from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.main),
    path("country/<int:country_id>/", views.get_country),
    path("media/<int:media_id>/", views.get_media),
    path("search/", views.search),
]
